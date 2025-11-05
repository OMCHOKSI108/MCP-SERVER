// Mock for VS Code API
export class Uri {
  static file(path: string): Uri {
    return new Uri('file', '', path);
  }

  static joinPath(base: Uri, ...pathSegments: string[]): Uri {
    const joined = [base.fsPath, ...pathSegments].join('/');
    // Normalize path separators for the current platform
    const normalized = joined.replace(/\/+/g, '/');
    return new Uri('file', '', normalized);
  }

  constructor(
    public readonly scheme: string,
    public readonly authority: string,
    public readonly path: string
  ) {}

  get fsPath(): string {
    // On Windows, VS Code returns backslashes
    return this.path.replace(/\//g, '\\');
  }
}

export const workspace = {
  fs: {
    stat: jest.fn(() => Promise.resolve()),
    copy: jest.fn(() => Promise.resolve()),
    createDirectory: jest.fn(() => Promise.resolve()),
    writeFile: jest.fn(() => Promise.resolve()),
    rename: jest.fn(() => Promise.resolve()),
    delete: jest.fn(() => Promise.resolve()),
    readFile: jest.fn(() => Promise.resolve(Buffer.from('')))
  },
  findFiles: jest.fn(() => Promise.resolve([])),
  asRelativePath: jest.fn((uri: Uri) => uri.fsPath)
};

export const window = {
  createOutputChannel: jest.fn(() => ({
    appendLine: jest.fn(),
    show: jest.fn()
  })),
  showInformationMessage: jest.fn(() => Promise.resolve(undefined)),
  showErrorMessage: jest.fn(() => Promise.resolve(undefined))
};