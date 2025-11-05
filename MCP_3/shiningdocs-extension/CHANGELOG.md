# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.0.1] - 2024-12-19

### Added
- Initial release of ShiningDocs VS Code extension
- Multi-provider AI support (Google Gemini, OpenAI GPT-4o, DeepSeek)
- Intelligent project analysis and documentation generation
- MkDocs-ready documentation site creation
- Secure API key management using VS Code secrets
- Modern webview UI integrated into sidebar
- Comprehensive error handling and user feedback
- Automated CI/CD pipeline with GitHub Actions
- 100% test coverage with unit and E2E tests
- Automated publishing workflow to VS Code Marketplace

### Features
- 🔍 **Project Scanning**: Automatically analyzes codebase structure and content
- 🤖 **AI Generation**: Uses advanced LLMs to create comprehensive documentation
- 📚 **MkDocs Integration**: Generates complete documentation sites ready for MkDocs
- 🔐 **Security**: Enterprise-grade API key storage and path validation
- ⚡ **Performance**: Optimized file operations with atomic writes and backups
- 🧪 **Testing**: Full test suite with automated validation
- 🚀 **Publishing**: Automated marketplace deployment

### Technical Details
- Built with TypeScript and VS Code Extension API
- Supports VS Code 1.74.0+
- Node.js 16.x+ required for development
- Comprehensive error handling with user-friendly messages
- Safe file operations with backup and rollback capabilities
- Modular architecture for maintainability and testing

### Known Issues
- None reported for initial release

### Dependencies
- @types/node: ^20.0.0
- @types/vscode: ^1.74.0
- @vscode/test-electron: ^2.3.0
- typescript: ^5.0.0
- jest: ^29.0.0
- ts-jest: ^29.0.0