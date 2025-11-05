import * as vscode from 'vscode';
import { ShiningDocsPanel } from './panels/ShiningDocsPanel';
import { generateDocs } from './core/generator';
import { getApiKey, saveApiKey } from './utils/secrets';

/**
 * Extension entry point - activates when commands are triggered
 */
export function activate(context: vscode.ExtensionContext) {
    console.log('ShiningDocs extension is now active!');

    // Create status bar item
    const statusBarItem = vscode.window.createStatusBarItem(vscode.StatusBarAlignment.Right, 100);
    statusBarItem.text = 'ShiningDocs: Ready';
    statusBarItem.show();
    context.subscriptions.push(statusBarItem);

    // Register commands
    const generateCommand = vscode.commands.registerCommand('shiningdocs.generate', async () => {
        await handleGenerateDocs(statusBarItem, context);
    });

    const openPanelCommand = vscode.commands.registerCommand('shiningdocs.openPanel', () => {
        ShiningDocsPanel.createOrShow(context.extensionUri, context);
    });

    // Register sidebar tree data provider
    const sidebarProvider = new ShiningDocsSidebarProvider();
    vscode.window.registerTreeDataProvider('shiningdocs.sidebar', sidebarProvider);

    // Add to subscriptions for cleanup
    context.subscriptions.push(generateCommand);
    context.subscriptions.push(openPanelCommand);
}

/**
 * Handles the generate documentation command
 */
async function handleGenerateDocs(statusBarItem: vscode.StatusBarItem, context: vscode.ExtensionContext) {
    const workspaceFolder = vscode.workspace.workspaceFolders?.[0];
    if (!workspaceFolder) {
        vscode.window.showErrorMessage('No workspace folder open');
        return;
    }

    try {
        // Get settings from webview (this would be passed via message)
        // For now, use placeholder values
        const model = 'gemini'; // TODO: get from webview
        const apiKey = await getApiKey(context);
        const projectContext = 'Project documentation'; // TODO: get from webview

        if (!apiKey) {
            vscode.window.showErrorMessage('API key not configured. Please set it in the ShiningDocs panel.');
            return;
        }

        statusBarItem.text = 'ShiningDocs: Scanning...';

        // Show progress
        await vscode.window.withProgress({
            location: vscode.ProgressLocation.Notification,
            title: 'Generating Documentation',
            cancellable: false
        }, async (progress) => {
            progress.report({ increment: 0, message: 'Analyzing project...' });

            // TODO: Implement actual doc generation
            await generateDocs(workspaceFolder.uri.fsPath, model, apiKey, projectContext);

            progress.report({ increment: 100, message: 'Documentation generated!' });
        });

        statusBarItem.text = 'ShiningDocs: Ready';
        vscode.window.showInformationMessage('Documentation generated successfully!');

    } catch (error) {
        statusBarItem.text = 'ShiningDocs: Error';
        vscode.window.showErrorMessage(`Failed to generate documentation: ${error}`);
    }
}

/**
 * Sidebar tree data provider for the ShiningDocs view
 */
class ShiningDocsSidebarProvider implements vscode.TreeDataProvider<SidebarItem> {
    getTreeItem(element: SidebarItem): vscode.TreeItem {
        return element;
    }

    getChildren(element?: SidebarItem): Thenable<SidebarItem[]> {
        if (!element) {
            // Root level - show main options
            return Promise.resolve([
                new SidebarItem('Generate Docs', 'Click to open the documentation generator panel', vscode.TreeItemCollapsibleState.None, {
                    command: 'shiningdocs.openPanel',
                    title: 'Open Panel'
                })
            ]);
        }
        return Promise.resolve([]);
    }
}

/**
 * Tree item for the sidebar
 */
class SidebarItem extends vscode.TreeItem {
    constructor(
        public override readonly label: string,
        public override readonly tooltip: string,
        public override readonly collapsibleState: vscode.TreeItemCollapsibleState,
        public override readonly command?: vscode.Command
    ) {
        super(label, collapsibleState);
        this.tooltip = tooltip;
        this.command = command;
    }
}

/**
 * Deactivates the extension
 */
export function deactivate() {
    console.log('ShiningDocs extension deactivated');
}