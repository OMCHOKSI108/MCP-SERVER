import { extractFilesFromText } from '../src/core/parser';

describe('extractFilesFromText', () => {
  it('parses ---FILE: markers (simple case)', () => {
    const input = `
---FILE: README.md---
# Project Title

---FILE: docs/installation.md---
## Install
1. Step A
`;
    const files = extractFilesFromText(input);
    expect(files).toHaveLength(2);
    const readme = files.find(f => f.path === 'README.md');
    expect(readme).toBeDefined();
    expect(readme!.content).toContain('# Project Title');
    const inst = files.find(f => f.path === 'docs/installation.md');
    expect(inst).toBeDefined();
    expect(inst!.content).toContain('## Install');
  });

  it('supports alternate marker syntaxes (<<<FILE: ... >>>)', () => {
    const input = `<<<FILE: docs/index.md>>>
# Index
`;
    const files = extractFilesFromText(input);
    expect(files.length).toBe(1);
    const file = files[0];
    expect(file).toBeDefined();
    if (file) {
      expect(file.path).toBe('docs/index.md');
      expect(file.content.trim()).toBe('# Index');
    }
  });

  it('returns empty array when no markers present', () => {
    const input = `# Whole content without markers

More text...`;
    const files = extractFilesFromText(input);
    expect(files.length).toBe(0);
  });

  it('trims content and preserves frontmatter', () => {
    const input = `---FILE: README.md---
---
title: Demo
---
# Hello
`;
    const files = extractFilesFromText(input);
    const readme = files.find(f => f.path === 'README.md')!;
    expect(readme.content.startsWith('---')).toBe(true);
    expect(readme.content).toContain('# Hello');
  });
});