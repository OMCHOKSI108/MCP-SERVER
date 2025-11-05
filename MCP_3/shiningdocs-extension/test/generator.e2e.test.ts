import { generateDocs } from '../src/core/generator';
import * as vscode from 'vscode';

// Mock LLM response with file markers
const MOCK_LLM_RESPONSE = `
---FILE: README.md---
# Test Project

This is a test project for ShiningDocs.

---FILE: docs/index.md---
# Documentation Index

Welcome to the documentation.

---FILE: mkdocs.yml---
site_name: Test Project
nav:
  - Home: index.md
  - Installation: installation.md
`;

// Mock scanned files
const MOCK_SCANNED_FILES = [
  {
    relativePath: 'package.json',
    content: '{"name": "test-project", "version": "1.0.0"}'
  },
  {
    relativePath: 'src/main.ts',
    content: 'console.log("Hello World");'
  }
];

describe('generateDocs E2E', () => {
  let mockFindFiles: jest.SpyInstance;
  let mockReadFile: jest.SpyInstance;
  let mockWriteFile: jest.SpyInstance;
  let mockCreateDirectory: jest.SpyInstance;
  let mockStat: jest.SpyInstance;
  let mockCopy: jest.SpyInstance;
  let mockRename: jest.SpyInstance;
  let mockDelete: jest.SpyInstance;
  let mockFetch: jest.SpyInstance;

  beforeEach(() => {
    // Mock VS Code workspace operations
    mockFindFiles = jest.spyOn(vscode.workspace, 'findFiles');
    mockReadFile = jest.spyOn(vscode.workspace.fs, 'readFile');
    mockWriteFile = jest.spyOn(vscode.workspace.fs, 'writeFile');
    mockCreateDirectory = jest.spyOn(vscode.workspace.fs, 'createDirectory');
    mockStat = jest.spyOn(vscode.workspace.fs, 'stat');
    mockCopy = jest.spyOn(vscode.workspace.fs, 'copy');
    mockRename = jest.spyOn(vscode.workspace.fs, 'rename');
    mockDelete = jest.spyOn(vscode.workspace.fs, 'delete');

    // Mock fetch for LLM API calls
    mockFetch = jest.spyOn(global, 'fetch');

    // Setup default mocks
    mockFindFiles.mockResolvedValue([
      vscode.Uri.file('/test-project/package.json'),
      vscode.Uri.file('/test-project/src/main.ts')
    ]);

    mockReadFile.mockImplementation((uri: vscode.Uri) => {
      if (uri.fsPath.includes('package.json')) {
        return Promise.resolve(Buffer.from(MOCK_SCANNED_FILES[0]?.content || ''));
      } else if (uri.fsPath.includes('main.ts')) {
        return Promise.resolve(Buffer.from(MOCK_SCANNED_FILES[1]?.content || ''));
      }
      return Promise.reject(new Error('File not found'));
    });

    // Files don't exist initially
    mockStat.mockRejectedValue(new Error('File does not exist'));

    // Mock successful LLM API response
    mockFetch.mockResolvedValue({
      ok: true,
      json: () => Promise.resolve({
        choices: [{ message: { content: MOCK_LLM_RESPONSE } }]
      })
    } as any);
  });

  afterEach(() => {
    jest.restoreAllMocks();
  });

  it('successfully generates documentation with OpenAI', async () => {
    const result = await generateDocs('/test-project', 'gpt-3.5-turbo', 'fake-api-key', 'Test context');

    // Verify result structure
    expect(result).toHaveProperty('filesWritten');
    expect(result).toHaveProperty('tokensUsed');
    expect(result).toHaveProperty('durationMs');
    expect(result).toHaveProperty('warnings');

    // Should have written 3 files (README.md, docs/index.md, mkdocs.yml)
    expect(result.filesWritten).toBe(3);
    expect(result.tokensUsed).toBeGreaterThan(0);
    expect(result.durationMs).toBeGreaterThan(0);
    expect(result.warnings).toHaveLength(0);

    // Verify workspace operations were called
    expect(mockFindFiles).toHaveBeenCalled();
    expect(mockReadFile).toHaveBeenCalledTimes(2); // Two files scanned
    expect(mockWriteFile).toHaveBeenCalledTimes(3); // Three files written
    expect(mockCreateDirectory).toHaveBeenCalled(); // Directory creation for docs/

    // Verify LLM API was called correctly
    expect(mockFetch).toHaveBeenCalledWith(
      'https://api.openai.com/v1/chat/completions',
      expect.objectContaining({
        method: 'POST',
        headers: expect.objectContaining({
          'Content-Type': 'application/json',
          'Authorization': 'Bearer fake-api-key'
        })
      })
    );
  });

  it('successfully generates documentation with Gemini', async () => {
    // Mock Gemini API response
    mockFetch.mockResolvedValue({
      ok: true,
      json: () => Promise.resolve({
        candidates: [{ content: { parts: [{ text: MOCK_LLM_RESPONSE }] } }]
      })
    } as any);

    const result = await generateDocs('/test-project', 'gemini-pro', 'fake-api-key', 'Test context');

    expect(result.filesWritten).toBe(3);
    expect(result.warnings).toHaveLength(0);

    // Verify Gemini API was called
    expect(mockFetch).toHaveBeenCalledWith(
      'https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key=fake-api-key',
      expect.any(Object)
    );
  });

  it('handles API errors gracefully', async () => {
    // Mock API failure
    mockFetch.mockResolvedValue({
      ok: false,
      status: 401,
      text: () => Promise.resolve('Invalid API key')
    } as any);

    const result = await generateDocs('/test-project', 'gpt-3.5-turbo', 'invalid-key', 'Test context');

    // Should return error result
    expect(result.filesWritten).toBe(0);
    expect(result.warnings).toHaveLength(1);
    expect(result.warnings[0]).toContain('Error');
  });

  it('creates backups when files already exist', async () => {
    // Mock that README.md already exists
    mockStat.mockImplementation((uri: vscode.Uri) => {
      if (uri.fsPath.includes('README.md')) {
        return Promise.resolve({} as any); // File exists
      }
      return Promise.reject(new Error('File does not exist'));
    });

    const result = await generateDocs('/test-project', 'gpt-3.5-turbo', 'fake-api-key', 'Test context');

    expect(result.filesWritten).toBe(3);
    // Should have created backup for README.md
    expect(mockCopy).toHaveBeenCalled();
    expect(result.warnings).toHaveLength(0);
  });

  it('handles network timeouts', async () => {
    // Mock network timeout
    mockFetch.mockImplementation(() => {
      return new Promise((_, reject) => {
        setTimeout(() => reject(new Error('Network timeout')), 100);
      });
    });

    const result = await generateDocs('/test-project', 'gpt-3.5-turbo', 'fake-api-key', 'Test context');

    expect(result.filesWritten).toBe(0);
    expect(result.warnings).toHaveLength(1);
    expect(result.warnings[0]).toContain('Error');
  });

  it('scans workspace correctly', async () => {
    const readFileCallCountBefore = mockReadFile.mock.calls.length;
    await generateDocs('/test-project', 'gpt-3.5-turbo', 'fake-api-key', 'Test context');
    const readFileCallCountAfter = mockReadFile.mock.calls.length;

    // Should have read 2 files during scanning
    expect(readFileCallCountAfter - readFileCallCountBefore).toBe(2);
  });

  it('handles unsupported model', async () => {
    const result = await generateDocs('/test-project', 'unsupported-model', 'fake-api-key', 'Test context');

    expect(result.filesWritten).toBe(0);
    expect(result.warnings).toHaveLength(1);
    expect(result.warnings[0]).toContain('Unsupported model');
  });
});