/*
PRO: Implement the ShiningDocs core generation engine.

🎯 Goal:
Build `generateDocs(projectRoot: Uri, model: string, apiKey: string, userContext: string)` that:
1) Scans the current VS Code workspace
2) Builds a summarized project context
3) Sends it to the chosen LLM (Gemini / OpenAI / DeepSeek)
4) Writes generated Markdown documentation into the workspace

🧩 Requirements:

A. Workspace Scanner
- Walk all files in projectRoot recursively using vscode.workspace.findFiles.
- Respect `.gitignore` and exclude: node_modules, .git, .venv, dist, build, coverage.
- Collect only relevant text files: .ts, .js, .py, .java, .go, package.json, requirements.txt.
- For each file: store relative path + first 2000 chars of content.
- Summarize structure in a tree string (indented paths).

B. Prompt Construction
- Create SYSTEM_PROMPT constant (see below).
- Build a user prompt containing:
  - UserContext
  - Project Structure
  - Code Snippets Summary
- Chunk large inputs if > 8 000 tokens (approx 24 000 chars).

C. LLM Call Adapter
- Implement `callLlm(model, apiKey, prompt): Promise<string>`
- Handle:
   - OpenAI API (POST https://api.openai.com/v1/chat/completions)
   - Gemini API (POST https://generativelanguage.googleapis.com/v1beta/models/[model]:generateContent)
   - DeepSeek API (similar OpenAI-style)
- Detect model by name; format request accordingly.
- Use fetch with proper headers and timeout (30 s).
- Handle rate limits / errors gracefully; show `vscode.window.showErrorMessage` on failure.

D. Output Writer
- Parse the LLM response text.
- If it includes `---FILE:` markers, split accordingly; otherwise:
  - create `README.md` and `docs/index.md`.
- Write files using `vscode.workspace.fs`.
- Back up existing docs as `.bak.<timestamp>` before overwriting.
- Show success info message with total files created.

E. System Prompt (Embed)
const SYSTEM_PROMPT = `
You are ShiningDocs, an expert technical writer.
Given the file structure and source code of a project, generate complete MkDocs documentation in Markdown:
- README.md
- docs/index.md
- docs/installation.md
- docs/usage.md
- docs/api_reference.md
Also generate mkdocs.yml and optionally .github/workflows/deploy.yml.
Do not invent features. Use only data from the provided project and user context.
`;

🧠 Design Hints:
- Separate each concern into helper functions:
   - scanWorkspace()
   - buildPrompt()
   - callLlm()
   - parseAndWrite()
- Return structured result: { filesWritten, tokensUsed, durationMs, warnings }.
- Use async/await and log steps to Output Channel "ShiningDocs".

📦 Output Expectation:
Fully typed TypeScript file with all helpers + exports, no external deps.
Include TODO comments for future tests and streaming support.
*/

import * as vscode from 'vscode';
import * as path from 'path';
import { parseAndWriteDocs } from './parser';

const SYSTEM_PROMPT = `
You are ShiningDocs, an expert technical writer.
Given the file structure and source code of a project, generate complete MkDocs documentation in Markdown:
- README.md
- docs/index.md
- docs/installation.md
- docs/usage.md
- docs/api_reference.md
Also generate mkdocs.yml and optionally .github/workflows/deploy.yml.
Do not invent features. Use only data from the provided project and user context.
`;

// File extensions to include in scanning
const INCLUDED_EXTENSIONS = ['.ts', '.js', '.py', '.java', '.go', '.json', '.txt', '.md', '.yml', '.yaml'];

// Directories to exclude
const EXCLUDED_DIRS = ['node_modules', '.git', '.venv', 'dist', 'build', 'coverage', '.next', '.nuxt', 'target', 'bin', 'obj'];

// Maximum content length per file
const MAX_FILE_CONTENT_LENGTH = 2000;

// Token approximation (rough estimate: 1 token ≈ 4 characters)
const MAX_PROMPT_CHARS = 24000;

/**
 * Result of the documentation generation process
 */
interface GenerationResult {
    filesWritten: number;
    tokensUsed: number;
    durationMs: number;
    warnings: string[];
}

/**
 * Represents a scanned file with its content
 */
interface ScannedFile {
    relativePath: string;
    content: string;
}

/**
 * Generates documentation for a project using AI
 */
export async function generateDocs(
    projectRoot: string,
    model: string,
    apiKey: string,
    userContext: string
): Promise<GenerationResult> {
    const startTime = Date.now();
    const outputChannel = vscode.window.createOutputChannel('ShiningDocs');
    outputChannel.show();

    try {
        outputChannel.appendLine('🔍 Starting workspace scan...');

        // Step 1: Scan workspace
        const scannedFiles = await scanWorkspace(projectRoot, outputChannel);

        // Step 2: Build prompt
        const prompt = buildPrompt(userContext, scannedFiles);

        // Step 3: Call LLM
        outputChannel.appendLine(`🤖 Calling ${model} API...`);
        const llmResponse = await callLlm(model, apiKey, prompt);

        // Step 4: Parse and write output
        const projectUri = vscode.Uri.file(projectRoot);
        const result = await parseAndWriteDocs(llmResponse, projectUri, {
            overwrite: true,
            backup: true,
            maxFileSize: 2000000 // 2MB
        });

        const duration = Date.now() - startTime;
        const tokensUsed = Math.ceil(prompt.length / 4); // Rough token estimation

        outputChannel.appendLine(`✅ Generation complete! ${result.writtenFiles.length} files written, ${result.backups.length} backups created in ${duration}ms`);

        return {
            filesWritten: result.writtenFiles.length,
            tokensUsed,
            durationMs: duration,
            warnings: result.warnings
        };

    } catch (error) {
        const duration = Date.now() - startTime;
        outputChannel.appendLine(`❌ Error: ${error}`);
        vscode.window.showErrorMessage(`ShiningDocs Error: ${error}`);

        return {
            filesWritten: 0,
            tokensUsed: 0,
            durationMs: duration,
            warnings: [`Error: ${error}`]
        };
    }
}

/**
 * Scans the workspace and collects relevant files
 */
async function scanWorkspace(projectRoot: string, outputChannel: vscode.OutputChannel): Promise<ScannedFile[]> {
    const scannedFiles: ScannedFile[] = [];
    const projectUri = vscode.Uri.file(projectRoot);

    // Build include pattern for relevant files
    const includePattern = `**/*{${INCLUDED_EXTENSIONS.join(',')}}`;

    // Build exclude patterns
    const excludePatterns = EXCLUDED_DIRS.map(dir => `**/${dir}/**`);
    const excludePattern = excludePatterns.length > 0 ? `{${excludePatterns.join(',')}}` : null;

    try {
        const files = await vscode.workspace.findFiles(includePattern, excludePattern, 1000);

        for (const fileUri of files) {
            try {
                const relativePath = path.relative(projectRoot, fileUri.fsPath);
                const content = await vscode.workspace.fs.readFile(fileUri);
                const contentString = content.toString();

                // Truncate content if too long
                const truncatedContent = contentString.length > MAX_FILE_CONTENT_LENGTH
                    ? contentString.substring(0, MAX_FILE_CONTENT_LENGTH) + '\n...[truncated]'
                    : contentString;

                scannedFiles.push({
                    relativePath,
                    content: truncatedContent
                });

            } catch (error) {
                outputChannel.appendLine(`⚠️  Failed to read ${fileUri.fsPath}: ${error}`);
            }
        }

        outputChannel.appendLine(`📁 Scanned ${scannedFiles.length} files`);

    } catch (error) {
        outputChannel.appendLine(`❌ Workspace scan failed: ${error}`);
        throw error;
    }

    return scannedFiles;
}

/**
 * Builds the prompt for the LLM
 */
function buildPrompt(userContext: string, scannedFiles: ScannedFile[]): string {
    // Build project structure tree
    const structureTree = buildStructureTree(scannedFiles);

    // Build code snippets summary
    const codeSnippets = scannedFiles
        .filter(file => !file.relativePath.includes('package.json') && !file.relativePath.includes('requirements.txt'))
        .slice(0, 10) // Limit to first 10 files to avoid token limits
        .map(file => `### ${file.relativePath}\n\`\`\`\n${file.content}\n\`\`\`\n`)
        .join('\n');

    // Build config files summary
    const configFiles = scannedFiles
        .filter(file => file.relativePath.includes('package.json') || file.relativePath.includes('requirements.txt'))
        .map(file => `### ${file.relativePath}\n\`\`\`\n${file.content}\n\`\`\`\n`)
        .join('\n');

    const prompt = `
User Context: ${userContext}

Project Structure:
${structureTree}

Configuration Files:
${configFiles}

Code Snippets (sample):
${codeSnippets}

Please generate complete MkDocs documentation for this project.
`;

    // Truncate if too long
    if (prompt.length > MAX_PROMPT_CHARS) {
        return prompt.substring(0, MAX_PROMPT_CHARS) + '\n\n[Content truncated due to length]';
    }

    return prompt;
}

/**
 * Builds a tree structure string from scanned files
 */
function buildStructureTree(scannedFiles: ScannedFile[]): string {
    const tree = new Map<string, any>();

    for (const file of scannedFiles) {
        const parts = file.relativePath.split(path.sep);
        let current: Map<string, any> = tree;

        for (let i = 0; i < parts.length; i++) {
            const part = parts[i];
            if (part && !current.has(part)) {
                current.set(part, i === parts.length - 1 ? true : new Map<string, any>());
            }
            if (part) {
                const next = current.get(part);
                if (next instanceof Map) {
                    current = next;
                } else {
                    break;
                }
            }
        }
    }

    return formatTree(tree, '', 0);
}

/**
 * Formats the tree Map into a string
 */
function formatTree(tree: Map<string, any>, prefix: string, depth: number): string {
    let result = '';
    const entries = Array.from(tree.entries()).sort(([a], [b]) => a.localeCompare(b));

    for (let i = 0; i < entries.length; i++) {
        const entryData = entries[i];
        if (!entryData) continue;

        const [entry, value] = entryData;
        const isLast = i === entries.length - 1;
        const connector = depth === 0 ? '' : (isLast ? '└── ' : '├── ');
        const nextPrefix = depth === 0 ? '' : prefix + (isLast ? '    ' : '│   ');

        result += prefix + connector + entry + '\n';

        if (value instanceof Map) {
            result += formatTree(value, nextPrefix, depth + 1);
        }
    }

    return result;
}

/**
 * Calls the appropriate LLM API based on the model
 */
async function callLlm(model: string, apiKey: string, prompt: string): Promise<string> {
    const timeout = 30000; // 30 seconds

    if (model.toLowerCase().includes('openai') || model.toLowerCase().includes('gpt')) {
        return await callOpenAI(model, apiKey, prompt, timeout);
    } else if (model.toLowerCase().includes('gemini')) {
        return await callGemini(model, apiKey, prompt, timeout);
    } else if (model.toLowerCase().includes('deepseek')) {
        return await callDeepSeek(model, apiKey, prompt, timeout);
    } else {
        throw new Error(`Unsupported model: ${model}`);
    }
}

/**
 * Calls OpenAI API
 */
async function callOpenAI(model: string, apiKey: string, prompt: string, timeout: number): Promise<string> {
    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), timeout);

    try {
        const response = await fetch('https://api.openai.com/v1/chat/completions', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${apiKey}`
            },
            body: JSON.stringify({
                model: model,
                messages: [
                    { role: 'system', content: SYSTEM_PROMPT },
                    { role: 'user', content: prompt }
                ],
                max_tokens: 4000,
                temperature: 0.7
            }),
            signal: controller.signal
        });

        clearTimeout(timeoutId);

        if (!response.ok) {
            const error = await response.text();
            throw new Error(`OpenAI API error: ${response.status} - ${error}`);
        }

        const data = await response.json();
        return data.choices[0]?.message?.content || '';

    } catch (error) {
        clearTimeout(timeoutId);
        if (error instanceof Error && error.name === 'AbortError') {
            throw new Error('OpenAI API request timed out');
        }
        throw error;
    }
}

/**
 * Calls Gemini API
 */
async function callGemini(model: string, apiKey: string, prompt: string, timeout: number): Promise<string> {
    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), timeout);

    // Extract model name (e.g., "gemini-pro" from "gemini-pro")
    const modelName = model.includes('-') ? model : 'gemini-pro';
    const url = `https://generativelanguage.googleapis.com/v1beta/models/${modelName}:generateContent?key=${apiKey}`;

    try {
        const response = await fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                contents: [{
                    parts: [{
                        text: SYSTEM_PROMPT + '\n\n' + prompt
                    }]
                }],
                generationConfig: {
                    temperature: 0.7,
                    maxOutputTokens: 4000
                }
            }),
            signal: controller.signal
        });

        clearTimeout(timeoutId);

        if (!response.ok) {
            const error = await response.text();
            throw new Error(`Gemini API error: ${response.status} - ${error}`);
        }

        const data = await response.json();
        return data.candidates[0]?.content?.parts[0]?.text || '';

    } catch (error) {
        clearTimeout(timeoutId);
        if (error instanceof Error && error.name === 'AbortError') {
            throw new Error('Gemini API request timed out');
        }
        throw error;
    }
}

/**
 * Calls DeepSeek API (OpenAI-compatible)
 */
async function callDeepSeek(model: string, apiKey: string, prompt: string, timeout: number): Promise<string> {
    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), timeout);

    try {
        const response = await fetch('https://api.deepseek.com/v1/chat/completions', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${apiKey}`
            },
            body: JSON.stringify({
                model: model,
                messages: [
                    { role: 'system', content: SYSTEM_PROMPT },
                    { role: 'user', content: prompt }
                ],
                max_tokens: 4000,
                temperature: 0.7
            }),
            signal: controller.signal
        });

        clearTimeout(timeoutId);

        if (!response.ok) {
            const error = await response.text();
            throw new Error(`DeepSeek API error: ${response.status} - ${error}`);
        }

        const data = await response.json();
        return data.choices[0]?.message?.content || '';

    } catch (error) {
        clearTimeout(timeoutId);
        if (error instanceof Error && error.name === 'AbortError') {
            throw new Error('DeepSeek API request timed out');
        }
        throw error;
    }
}

// TODO: Add unit tests for all functions
// TODO: Implement streaming support for large responses
// TODO: Add support for custom templates
// TODO: Implement caching for repeated scans