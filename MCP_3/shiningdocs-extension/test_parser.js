// Simple test for the parser functionality
import * as vscode from 'vscode';
import { parseAndWriteDocs, extractFilesFromText } from '../src/core/parser';

// Test the file extraction
const testResponse = `---FILE: README.md---
# Test Project

This is a test README.

---FILE: docs/index.md---
# Welcome

Welcome to docs.
`;

console.log('Testing extractFilesFromText:');
const files = extractFilesFromText(testResponse);
console.log('Extracted files:', files);

// Test with vscode URI (would need actual VS Code environment)
// const testUri = vscode.Uri.file('D:\\WORKSPACE\\MCP\\test-output');
// parseAndWriteDocs(testResponse, testUri).then(result => {
//     console.log('Parse result:', result);
// });