"use strict";
var __createBinding = (this && this.__createBinding) || (Object.create ? (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    var desc = Object.getOwnPropertyDescriptor(m, k);
    if (!desc || ("get" in desc ? !m.__esModule : desc.writable || desc.configurable)) {
      desc = { enumerable: true, get: function() { return m[k]; } };
    }
    Object.defineProperty(o, k2, desc);
}) : (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    o[k2] = m[k];
}));
var __setModuleDefault = (this && this.__setModuleDefault) || (Object.create ? (function(o, v) {
    Object.defineProperty(o, "default", { enumerable: true, value: v });
}) : function(o, v) {
    o["default"] = v;
});
var __importStar = (this && this.__importStar) || function (mod) {
    if (mod && mod.__esModule) return mod;
    var result = {};
    if (mod != null) for (var k in mod) if (k !== "default" && Object.prototype.hasOwnProperty.call(mod, k)) __createBinding(result, mod, k);
    __setModuleDefault(result, mod);
    return result;
};
Object.defineProperty(exports, "__esModule", { value: true });
const path = __importStar(require("path"));
const vscode = __importStar(require("vscode"));
const parser_1 = require("../src/core/parser");
describe('safeJoinRoot', () => {
    // Node environment — construct a fake Uri
    const root = vscode.Uri.file(path.join('/', 'tmp', 'project-root'));
    it('joins safe relative paths', () => {
        const res = (0, parser_1.safeJoinRoot)(root, 'docs/index.md');
        expect(res).not.toBeNull();
        expect(res.fsPath).toContain(path.join('tmp', 'project-root', 'docs', 'index.md'));
    });
    it('rejects path traversal attempts', () => {
        const res = (0, parser_1.safeJoinRoot)(root, '../secrets.txt');
        expect(res).toBeNull();
    });
    it('rejects absolute paths', () => {
        const res = (0, parser_1.safeJoinRoot)(root, path.resolve('/etc/passwd'));
        expect(res).toBeNull();
    });
    it('normalizes weird separators', () => {
        const res = (0, parser_1.safeJoinRoot)(root, 'docs\\..\\docs2/../README.md');
        // should be normalized inside project root, not escape to parent
        expect(res).not.toBeNull();
        expect(res.fsPath).toContain(path.join('tmp', 'project-root'));
    });
});
//# sourceMappingURL=parser.safeJoin.test.js.map