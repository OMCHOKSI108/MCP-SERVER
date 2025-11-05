"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
const parser_1 = require("../src/core/parser");
describe('extractFilesFromText', () => {
    it('parses ---FILE: markers (simple case)', () => {
        const input = `
---FILE: README.md---
# Project Title

---FILE: docs/installation.md---
## Install
1. Step A
`;
        const files = (0, parser_1.extractFilesFromText)(input);
        expect(files).toHaveLength(2);
        const readme = files.find(f => f.path === 'README.md');
        expect(readme).toBeDefined();
        expect(readme.content).toContain('# Project Title');
        const inst = files.find(f => f.path === 'docs/installation.md');
        expect(inst).toBeDefined();
        expect(inst.content).toContain('## Install');
    });
    it('supports alternate marker syntaxes (<<<FILE: ... >>>)', () => {
        const input = `<<<FILE: docs/index.md>>>
# Index
`;
        const files = (0, parser_1.extractFilesFromText)(input);
        expect(files.length).toBe(1);
        const file = files[0];
        expect(file).toBeDefined();
        if (file) {
            expect(file.path).toBe('docs/index.md');
            expect(file.content.trim()).toBe('# Index');
        }
    });
    it('falls back when no markers present', () => {
        const input = `# Whole content without markers

More text...`;
        const files = (0, parser_1.extractFilesFromText)(input);
        // fallback behavior should create at least README.md
        expect(files.length).toBeGreaterThan(0);
        expect(files.some(f => f.path === 'README.md')).toBe(true);
    });
    it('trims content and preserves frontmatter', () => {
        const input = `---FILE: README.md---
---
title: Demo
---
# Hello
`;
        const files = (0, parser_1.extractFilesFromText)(input);
        const readme = files.find(f => f.path === 'README.md');
        expect(readme.content.startsWith('---')).toBe(true);
        expect(readme.content).toContain('# Hello');
    });
});
//# sourceMappingURL=parser.extract.test.js.map