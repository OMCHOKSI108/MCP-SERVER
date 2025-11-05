import * as vscode from 'vscode';

/**
 * Saves an API key securely using VS Code secrets
 */
export async function saveApiKey(context: vscode.ExtensionContext, apiKey: string): Promise<void> {
    await context.secrets.store('shiningdocs.apiKey', apiKey);
}

/**
 * Retrieves the stored API key
 */
export async function getApiKey(context: vscode.ExtensionContext): Promise<string | undefined> {
    return await context.secrets.get('shiningdocs.apiKey');
}

/**
 * Deletes the stored API key
 */
export async function deleteApiKey(context: vscode.ExtensionContext): Promise<void> {
    await context.secrets.delete('shiningdocs.apiKey');
}