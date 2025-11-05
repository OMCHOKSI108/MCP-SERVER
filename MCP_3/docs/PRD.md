🧭 Product Requirements Document (PRD)
Project: ShiningDocs

Tagline: “Your AI-powered documentation co-pilot for VS Code — 100% local, open-source, and zero-cost.”

1. Objective

Create an open-source VS Code extension that automatically generates complete project documentation (README + mkdocs site) using an LLM chosen by the user.
The extension runs locally, scans the codebase, and sends relevant code + structure to the LLM via the user’s own API key.

2. Key Features
Feature	Description
🧩 Local Project Scan	Reads all project files using vscode.workspace while ignoring system and irrelevant directories (node_modules, .git, .venv, etc.)
🧠 Bring Your Own Key (BYOK)	User inputs their API key (OpenAI, Gemini, DeepSeek, etc.) which is stored securely using vscode.secrets
⚙️ Multi-Model Support	Dropdown for model selection: Gemini, GPT-4o, DeepSeek, Claude, etc.
🪄 Prompt Engineering Engine	Builds contextual prompts combining project code + user notes
🗂️ Markdown Generation	AI generates README.md + mkdocs folder structure (docs/index.md, installation.md, usage.md, api_reference.md)
🚀 Auto Deployment Ready	Generates mkdocs.yml + optional .github/workflows/deploy.yml for GitHub Pages auto-deploy
🔒 100% Local Processing	No remote servers — all logic and API calls are executed inside the VS Code client
🌐 Marketplace Distribution	Distributed via VS Code Marketplace (no custom website needed)
3. System Architecture
🧱 Component 1: VS Code Extension (Frontend + Local Server)

Built With: TypeScript, VS Code Extension API

Panels:

Settings View:

Model selector (<select>)

API key input (<input type="password">)

Control Panel:

Project context <textarea>

“Generate Docs” button

⚙️ Component 2: MCP Agent (Core Logic Engine)

Flow:

Read user configuration (model + API key).

Scan workspace (using vscode.workspace.findFiles() with .gitignore filter).

Build project summary (folder tree + key files).

Construct prompt:

System Prompt: “You are ShiningDocs, an expert technical writer...”

User Prompt: includes custom context + selected code.

Make API request using fetch() directly from VS Code.

Parse and write response to local files (README.md, docs/, mkdocs.yml).

🧭 Component 3: Deployment Integration

Auto-create mkdocs.yml

Optional .github/workflows/deploy.yml

Optional mkdocs serve quick command via VS Code command palette.

4. User Flow

Install Extension: Search “ShiningDocs” on Marketplace → Install.

Setup: Open sidebar → Select model → Enter API key → Save.

Context: Add short description in textarea.

Generate: Click “Generate Documentation.”

Result: Docs folder + README.md auto-created with complete site structure.

(Optional): Run mkdocs serve locally or push to GitHub for auto-deploy.

5. Example System Prompt
You are **ShiningDocs**, an expert AI technical writer.

You will be given the **complete file structure and codebase** of a project along with a short user description.

Your task:
- Create full project documentation suitable for **MkDocs**.
- Output strictly in Markdown format.

Your deliverables must include:
1. README.md (project summary, features, setup, usage, contribution)
2. /docs folder containing:
   - index.md (overview)
   - installation.md
   - usage.md
   - api_reference.md
3. mkdocs.yml configuration file
4. Optional .github/workflows/deploy.yml for GitHub Pages deployment

Follow industry documentation standards. Use clear section headings, example snippets, and consistent formatting.
Do not invent features. Derive all content strictly from code and user context.

6. Technical Stack
Component	Technology
VS Code Extension	TypeScript + VS Code API
Secrets Storage	vscode.secrets
File System Access	vscode.workspace.fs
API Requests	Native fetch()
Config Parsing	JSON + .gitignore parser
Markdown Output	Plain Markdown files
7. Data Flow Diagram
[User] 
   ↓
[VS Code Extension UI]
   ↓
[ShiningDocs MCP Agent]
   ↓
[Code Scanner] —> Builds code map
   ↓
[Prompt Builder]
   ↓
[LLM API (via user key)]
   ↓
[Response Parser]
   ↓
[File Writer]
   ↓
[Generated Docs + mkdocs.yml]

8. Security & Privacy

No telemetry or data upload.

User API keys stored securely via vscode.secrets.

All API calls happen locally.

Open-source repository ensures full transparency.

9. Future Roadmap (Post v1)
Version	Feature
v1.0	Core doc generation (README + docs/)
v1.1	Theme customization for mkdocs
v1.2	AI summary previews in VS Code panel
v2.0	Multi-language doc generation (English + Hindi + Japanese)
v2.1	Custom templates for different project types (Flask, React, etc.)
10. Deliverables for MVP

✅ VS Code Extension source (TypeScript)
✅ README.md (for extension repo)
✅ package.json (extension manifest)
✅ Core logic for:

workspace scanning

prompt assembly

LLM API calling

markdown file writing
✅ Marketplace publish-ready version

✅ System Prompt (for VS Code Extension Logic)
const SYSTEM_PROMPT = `
You are ShiningDocs, an AI-powered documentation generator.
Given the file structure and code of a project, generate complete, professional documentation for MkDocs.
Include:
- README.md
- docs/index.md
- docs/installation.md
- docs/usage.md
- docs/api_reference.md
Also output mkdocs.yml and optionally .github/workflows/deploy.yml.
Use clean Markdown. Do not add fictional features. Follow real code and user context strictly.
`;
