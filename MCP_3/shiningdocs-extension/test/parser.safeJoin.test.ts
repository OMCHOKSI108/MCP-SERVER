import * as path from 'path';
import * as vscode from 'vscode';
import { safeJoinRoot } from '../src/core/parser';

describe('safeJoinRoot', () => {
  // Node environment — construct a fake Uri
  const root = vscode.Uri.file(path.join('/', 'tmp', 'project-root'));

  it('joins safe relative paths', () => {
    const res = safeJoinRoot(root, 'docs/index.md');
    expect(res).not.toBeNull();
    expect(res!.fsPath).toContain(path.join('tmp', 'project-root', 'docs', 'index.md'));
  });

  it('rejects path traversal attempts', () => {
    const res = safeJoinRoot(root, '../secrets.txt');
    expect(res).toBeNull();
  });

  it('rejects absolute paths', () => {
    const res = safeJoinRoot(root, path.resolve('/etc/passwd'));
    expect(res).toBeNull();
  });

  it('normalizes weird separators', () => {
    const res = safeJoinRoot(root, 'docs\\..\\docs2/../README.md');
    // should be normalized inside project root, not escape to parent
    expect(res).not.toBeNull();
    expect(res!.fsPath).toContain(path.join('tmp', 'project-root'));
  });
});