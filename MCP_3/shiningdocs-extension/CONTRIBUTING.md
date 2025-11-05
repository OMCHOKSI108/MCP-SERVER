# Contributing to ShiningDocs

Thank you for your interest in contributing to ShiningDocs! We welcome contributions from the community to help make this extension better.

## 🚀 Quick Start

1. **Fork the repository** on GitHub
2. **Clone your fork** locally:
   ```bash
   git clone https://github.com/your-username/shiningdocs.git
   cd shiningdocs
   ```
3. **Install dependencies**:
   ```bash
   npm install
   ```
4. **Create a feature branch**:
   ```bash
   git checkout -b feature/your-feature-name
   ```
5. **Make your changes** and ensure tests pass:
   ```bash
   npm run test
   npm run compile
   ```
6. **Commit your changes**:
   ```bash
   git commit -m "Add your descriptive commit message"
   ```
7. **Push to your fork**:
   ```bash
   git push origin feature/your-feature-name
   ```
8. **Create a Pull Request** on GitHub

## 🛠️ Development Setup

### Prerequisites
- Node.js 16.x or later
- VS Code 1.74.0 or later
- Git

### Building the Extension
```bash
# Install dependencies
npm install

# Compile TypeScript
npm run compile

# Watch for changes during development
npm run watch
```

### Running Tests
```bash
# Run all tests
npm run test

# Run tests in watch mode
npm run test:watch

# Run tests with coverage
npm run test:coverage
```

### Debugging
1. Press `F5` in VS Code to launch Extension Development Host
2. Open a workspace folder for testing
3. Use the sidebar to access ShiningDocs features
4. Check the "ShiningDocs" output channel for logs

## 📋 Code Guidelines

### TypeScript Standards
- Use strict TypeScript with no `any` types
- Add proper JSDoc comments for public APIs
- Follow VS Code extension API patterns
- Use async/await for asynchronous operations

### Testing Requirements
- Write unit tests for all new functions
- Include E2E tests for new features
- Maintain 100% test coverage
- Use descriptive test names

### Error Handling
- Never throw unhandled exceptions
- Use VS Code's error reporting APIs
- Provide user-friendly error messages
- Log errors to output channel for debugging

### Security
- Never log sensitive information (API keys, etc.)
- Use VS Code's secret storage for sensitive data
- Validate all file paths and user inputs
- Follow secure coding practices

## 🎯 Contribution Types

### 🐛 Bug Fixes
- Fix reported issues
- Add regression tests
- Update documentation if needed

### ✨ New Features
- Discuss feature ideas in Issues first
- Implement with comprehensive tests
- Update README and CHANGELOG
- Follow existing code patterns

### 📚 Documentation
- Improve README, guides, or code comments
- Add examples or tutorials
- Fix typos or clarify explanations

### 🧪 Testing
- Add missing test coverage
- Improve test reliability
- Add integration tests

### 🔧 Maintenance
- Update dependencies
- Improve build process
- Code refactoring and cleanup

## 📝 Pull Request Process

1. **Ensure your PR**:
   - Has a clear, descriptive title
   - Includes a detailed description of changes
   - References any related issues
   - Passes all tests and linting
   - Follows the code guidelines above

2. **PR Template**:
   - **What**: Brief description of changes
   - **Why**: Reason for the changes
   - **How**: Implementation details
   - **Testing**: How changes were tested

3. **Review Process**:
   - Automated checks must pass (CI, tests, linting)
   - At least one maintainer review required
   - Address review feedback promptly
   - Squash commits if requested

## 🎉 Recognition

Contributors will be:
- Listed in CHANGELOG.md for significant contributions
- Mentioned in release notes
- Added to a future contributors file

## 📞 Getting Help

- **Issues**: Report bugs or request features
- **Discussions**: Ask questions or share ideas
- **Discord**: Join our community chat (coming soon)

## 📜 License

By contributing, you agree that your contributions will be licensed under the same MIT License that covers the project.

Thank you for helping make ShiningDocs better! 🚀