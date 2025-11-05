import * as vscode from 'vscode';
import { saveApiKey, getApiKey } from '../utils/secrets';

/**
 * Interface for messages sent from webview to extension
 */
interface WebviewMessage {
    command: string;
    data?: any;
}

/**
 * Interface for generation settings
 */
interface GenerationSettings {
    model: string;
    apiKey: string;
    context: string;
}

/**
 * Manages the ShiningDocs webview panel
 */
export class ShiningDocsPanel {
    public static currentPanel: ShiningDocsPanel | undefined;
    public static readonly viewType = 'shiningdocs.panel';

    private readonly _panel: vscode.WebviewPanel;
    private readonly _extensionUri: vscode.Uri;
    private readonly _context: vscode.ExtensionContext;
    private _disposables: vscode.Disposable[] = [];

    /**
     * Creates or shows the webview panel
     */
    public static createOrShow(extensionUri: vscode.Uri, context: vscode.ExtensionContext) {
        const column = vscode.window.activeTextEditor
            ? vscode.window.activeTextEditor.viewColumn
            : undefined;

        // If we already have a panel, show it
        if (ShiningDocsPanel.currentPanel) {
            ShiningDocsPanel.currentPanel._panel.reveal(column);
            return;
        }

        // Otherwise, create a new panel
        const panel = vscode.window.createWebviewPanel(
            ShiningDocsPanel.viewType,
            'ShiningDocs',
            column || vscode.ViewColumn.One,
            {
                enableScripts: true,
                localResourceRoots: [vscode.Uri.joinPath(extensionUri, 'media')]
            }
        );

        ShiningDocsPanel.currentPanel = new ShiningDocsPanel(panel, extensionUri, context);
    }

    /**
     * Constructor - private to enforce singleton pattern
     */
    private constructor(panel: vscode.WebviewPanel, extensionUri: vscode.Uri, context: vscode.ExtensionContext) {
        this._panel = panel;
        this._extensionUri = extensionUri;
        this._context = context;

        // Set the webview's initial html content
        this._update();

        // Listen for when the panel is disposed
        // This happens when the user closes the panel or when the panel is closed programmatically
        this._panel.onDidDispose(() => this.dispose(), null, this._disposables);

        // Handle messages from the webview
        this._panel.webview.onDidReceiveMessage(
            async (message: WebviewMessage) => {
                await this._handleMessage(message);
            },
            null,
            this._disposables
        );
    }

    /**
     * Handles messages from the webview
     */
    private async _handleMessage(message: WebviewMessage) {
        switch (message.command) {
            case 'generate':
                await this._handleGenerate(message.data);
                break;
            case 'saveApiKey':
                await this._handleSaveApiKey(message.data);
                break;
            case 'loadSettings':
                await this._handleLoadSettings();
                break;
        }
    }

    /**
     * Handles the generate documentation request
     */
    private async _handleGenerate(settings: GenerationSettings) {
        // Update status in webview
        this._panel.webview.postMessage({ command: 'status', text: 'Generating docs...' });

        try {
            // Trigger the generate command with settings
            await vscode.commands.executeCommand('shiningdocs.generate', settings);

            // Update status on success
            this._panel.webview.postMessage({ command: 'status', text: 'Documentation generated successfully!' });
        } catch (error) {
            // Update status on error
            this._panel.webview.postMessage({ command: 'status', text: `Error: ${error}` });
        }
    }

    /**
     * Handles saving the API key
     */
    private async _handleSaveApiKey(apiKey: string) {
        try {
            await saveApiKey(this._context, apiKey);
            this._panel.webview.postMessage({ command: 'apiKeySaved', success: true });
        } catch (error) {
            this._panel.webview.postMessage({ command: 'apiKeySaved', success: false, error: error });
        }
    }

    /**
     * Handles loading current settings
     */
    private async _handleLoadSettings() {
        try {
            const apiKey = await getApiKey(this._context);
            const settings = {
                model: 'gemini',
                context: '',
                hasApiKey: !!apiKey
            };
            this._panel.webview.postMessage({ command: 'settingsLoaded', settings });
        } catch (error) {
            this._panel.webview.postMessage({ command: 'settingsLoaded', settings: { model: 'gemini', context: '', hasApiKey: false } });
        }
    }

    /**
     * Updates the webview content
     */
    private _update() {
        const webview = this._panel.webview;
        this._panel.title = 'ShiningDocs';
        this._panel.webview.html = this._getHtmlForWebview(webview);
    }

    /**
     * Generates the HTML content for the webview
     */
    private _getHtmlForWebview(webview: vscode.Webview) {
        // Get the local path to main script run in the webview, then convert it to a uri we can use in the webview.
        const scriptUri = webview.asWebviewUri(vscode.Uri.joinPath(this._extensionUri, 'media', 'main.js'));

        // Do the same for the stylesheet.
        const styleUri = webview.asWebviewUri(vscode.Uri.joinPath(this._extensionUri, 'media', 'style.css'));

        // Use a nonce to only allow specific scripts to be run
        const nonce = getNonce();

        return `<!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <meta http-equiv="Content-Security-Policy" content="default-src 'none'; style-src ${webview.cspSource}; script-src 'nonce-${nonce}';">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <link href="${styleUri}" rel="stylesheet">
                <title>ShiningDocs</title>
            </head>
            <body>
                <div class="container">
                    <h1>ShiningDocs</h1>
                    <p>Generate AI-powered documentation for your project</p>

                    <div class="form-group">
                        <label for="model">AI Model:</label>
                        <select id="model">
                            <option value="gemini">Gemini</option>
                            <option value="openai">OpenAI GPT-4o</option>
                            <option value="deepseek">DeepSeek</option>
                        </select>
                    </div>

                    <div class="form-group">
                        <label for="apiKey">API Key:</label>
                        <input type="password" id="apiKey" placeholder="Enter your API key">
                        <button id="saveApiKey">Save Key</button>
                    </div>

                    <div class="form-group">
                        <label for="context">Project Context:</label>
                        <textarea id="context" rows="4" placeholder="Describe your project, goals, and any specific documentation requirements..."></textarea>
                    </div>

                    <button id="generate" class="primary-button">Generate Docs</button>

                    <div id="status" class="status">Ready</div>
                </div>

                <script nonce="${nonce}" src="${scriptUri}"></script>
            </body>
            </html>`;
    }

    /**
     * Disposes the panel and cleans up resources
     */
    public dispose() {
        ShiningDocsPanel.currentPanel = undefined;

        // Clean up our resources
        this._panel.dispose();

        while (this._disposables.length) {
            const x = this._disposables.pop();
            if (x) {
                x.dispose();
            }
        }
    }
}

/**
 * Generates a nonce for CSP
 */
function getNonce() {
    let text = '';
    const possible = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
    for (let i = 0; i < 32; i++) {
        text += possible.charAt(Math.floor(Math.random() * possible.length));
    }
    return text;
}