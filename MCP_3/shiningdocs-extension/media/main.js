// ShiningDocs Webview JavaScript

(function() {
    'use strict';

    // Get DOM elements
    const modelSelect = document.getElementById('model');
    const apiKeyInput = document.getElementById('apiKey');
    const saveApiKeyButton = document.getElementById('saveApiKey');
    const contextTextarea = document.getElementById('context');
    const generateButton = document.getElementById('generate');
    const statusDiv = document.getElementById('status');

    // Initialize
    document.addEventListener('DOMContentLoaded', function() {
        setupEventListeners();
        loadSettings();
    });

    /**
     * Sets up event listeners for UI elements
     */
    function setupEventListeners() {
        saveApiKeyButton.addEventListener('click', handleSaveApiKey);
        generateButton.addEventListener('click', handleGenerate);
    }

    /**
     * Loads current settings from the extension
     */
    function loadSettings() {
        // Request settings from extension
        vscode.postMessage({
            command: 'loadSettings'
        });
    }

    /**
     * Handles saving the API key
     */
    function handleSaveApiKey() {
        const apiKey = apiKeyInput.value.trim();
        if (!apiKey) {
            showStatus('Please enter an API key', 'error');
            return;
        }

        // Send save request to extension
        vscode.postMessage({
            command: 'saveApiKey',
            data: apiKey
        });
    }

    /**
     * Handles the generate documentation request
     */
    function handleGenerate() {
        const model = modelSelect.value;
        const apiKey = apiKeyInput.value.trim();
        const context = contextTextarea.value.trim();

        if (!apiKey) {
            showStatus('Please enter and save your API key', 'error');
            return;
        }

        if (!context) {
            showStatus('Please provide project context', 'error');
            return;
        }

        // Update UI
        generateButton.disabled = true;
        showStatus('Generating docs...', 'generating');

        // Send generate request to extension
        vscode.postMessage({
            command: 'generate',
            data: {
                model: model,
                apiKey: apiKey,
                context: context
            }
        });
    }

    /**
     * Updates the status display
     */
    function showStatus(text, type = 'ready') {
        statusDiv.textContent = text;
        statusDiv.className = `status ${type}`;
    }

    /**
     * Handles messages from the extension
     */
    window.addEventListener('message', event => {
        const message = event.data;

        switch (message.command) {
            case 'status':
                showStatus(message.text, getStatusType(message.text));
                if (message.text.includes('successfully') || message.text.includes('Error')) {
                    generateButton.disabled = false;
                }
                break;
            case 'apiKeySaved':
                if (message.success) {
                    showStatus('API key saved successfully', 'success');
                    setTimeout(() => showStatus('Ready'), 2000);
                } else {
                    showStatus('Failed to save API key', 'error');
                }
                break;
            case 'settingsLoaded':
                // Populate form with loaded settings
                if (message.settings) {
                    modelSelect.value = message.settings.model || 'gemini';
                    contextTextarea.value = message.settings.context || '';
                }
                break;
        }
    });

    /**
     * Determines status type based on message content
     */
    function getStatusType(text) {
        if (text.includes('Error') || text.includes('Failed')) {
            return 'error';
        } else if (text.includes('Generating')) {
            return 'generating';
        } else if (text.includes('successfully')) {
            return 'success';
        }
        return 'ready';
    }

})();