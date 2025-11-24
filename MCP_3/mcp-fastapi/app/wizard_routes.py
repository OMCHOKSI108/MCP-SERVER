"""Wizard routes for project setup."""
import json
import os
from pathlib import Path
from fastapi import APIRouter, Request, HTTPException, Form
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from pydantic import ValidationError

from app.project_manager import project_manager, ProjectConfig

router = APIRouter()

# Setup templates
templates_dir = Path(__file__).parent / "templates"
templates_dir.mkdir(exist_ok=True)
templates = Jinja2Templates(directory=str(templates_dir))

# Create wizard HTML template
wizard_html = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SensCoder MCP - Project Setup</title>
    <link rel="stylesheet" href="https://unpkg.com/lucide@latest/dist/umd/lucide.css">
    <script src="https://unpkg.com/lucide@latest/dist/umd/lucide.js"></script>
        :root {
            --bg: #f5f7ff;
            --bg-card: #ffffff;
            --accent: #4f46e5;
            --accent-soft: #e0e7ff;
            --text-main: #111827;
            --text-muted: #6b7280;
            --border-subtle: #e5e7eb;
            --shadow-soft: 0 18px 40px rgba(15, 23, 42, 0.12);
            --radius-lg: 18px;
            --radius-xl: 22px;
        }

        * {
            box-sizing: border-box;
        }

        body {
            margin: 0;
            font-family: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
            background: radial-gradient(circle at top left, #e3f2ff, transparent 60%),
                        radial-gradient(circle at bottom right, #fce7ff, transparent 55%),
                        var(--bg);
            color: var(--text-main);
            min-height: 100vh;
        }

        .page {
            min-height: 100vh;
            display: flex;
            flex-direction: column;
        }

        /* Header */
        .header {
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 16px 32px;
            background: rgba(248, 250, 252, 0.85);
            backdrop-filter: blur(12px);
            border-bottom: 1px solid rgba(148, 163, 184, 0.25);
        }

        .brand {
            display: flex;
            align-items: center;
            gap: 10px;
        }

        .brand-logo {
            width: 32px;
            height: 32px;
            border-radius: 999px;
            background: linear-gradient(135deg, #4f46e5, #6366f1);
            display: flex;
            align-items: center;
            justify-content: center;
            color: #ffffff;
            font-weight: 700;
            font-size: 14px;
            box-shadow: 0 10px 24px rgba(79, 70, 229, 0.45);
        }

        .brand-logo .logo-icon {
            width: 18px;
            height: 18px;
        }

        .brand-text-title {
            font-weight: 600;
            letter-spacing: 0.02em;
        }

        .brand-text-sub {
            font-size: 12px;
            color: var(--text-muted);
        }

        /* Tabs */
        .tabs {
            display: inline-flex;
            padding: 4px;
            border-radius: 999px;
            background: rgba(255, 255, 255, 0.9);
            box-shadow: 0 14px 30px rgba(15, 23, 42, 0.14);
            margin: 28px auto;
        }

        .tab {
            border: none;
            outline: none;
            padding: 10px 20px;
            display: inline-flex;
            align-items: center;
            gap: 8px;
            border-radius: 999px;
            font-size: 14px;
            cursor: pointer;
            background: transparent;
            color: var(--text-muted);
            transition: all 0.18s ease;
            white-space: nowrap;
        }

        .tab .icon {
            width: 16px;
            height: 16px;
        }

        .tab.active {
            background: linear-gradient(135deg, #4f46e5, #a855f7);
            color: #ffffff;
            box-shadow: 0 10px 26px rgba(76, 81, 191, 0.5);
        }

        .tab:not(.active):hover {
            background: rgba(243, 244, 246, 0.95);
            color: #111827;
        }

        /* Main content */
        .main {
            flex: 1;
            padding: 0 24px 40px;
            display: flex;
            justify-content: center;
        }

        .content {
            width: 100%;
            max-width: 800px;
        }

        /* Card */
        .card {
            background: linear-gradient(145deg, #ffffff, #f4f4ff);
            border-radius: var(--radius-xl);
            padding: 32px;
            box-shadow: var(--shadow-soft);
            border: 1px solid rgba(226, 232, 240, 0.9);
        }

        .card-header {
            text-align: center;
            margin-bottom: 32px;
        }

        .card-header h1 {
            font-size: 28px;
            letter-spacing: 0.02em;
            margin-bottom: 8px;
        }

        .card-header p {
            font-size: 16px;
            color: var(--text-muted);
        }

        /* Form elements */
        .form-group {
            margin-bottom: 24px;
        }

        .form-group label {
            display: block;
            font-weight: 600;
            color: var(--text-main);
            margin-bottom: 8px;
        }

        .form-group input {
            width: 100%;
            padding: 12px 16px;
            border: 2px solid var(--border-subtle);
            border-radius: 12px;
            font-size: 16px;
            transition: border-color 0.2s;
        }

        .form-group input:focus {
            outline: none;
            border-color: var(--accent);
        }

        /* Buttons */
        .btn-primary {
            padding: 16px 24px;
            border-radius: 999px;
            border: none;
            outline: none;
            cursor: pointer;
            font-size: 16px;
            font-weight: 600;
            background: linear-gradient(135deg, #4f46e5, #a855f7);
            color: #ffffff;
            display: inline-flex;
            align-items: center;
            gap: 8px;
            box-shadow: 0 12px 25px rgba(79, 70, 229, 0.4);
            transition: transform 0.12s ease, box-shadow 0.12s ease;
            white-space: nowrap;
        }

        .btn-primary:hover {
            transform: translateY(-2px);
            filter: brightness(1.03);
            box-shadow: 0 16px 30px rgba(79, 70, 229, 0.5);
        }

        .btn-primary:disabled {
            opacity: 0.6;
            cursor: not-allowed;
            transform: none;
        }

        .btn-secondary {
            padding: 16px 24px;
            border-radius: 999px;
            border: 2px solid var(--accent);
            outline: none;
            cursor: pointer;
            font-size: 16px;
            font-weight: 600;
            background: transparent;
            color: var(--accent);
            display: inline-flex;
            align-items: center;
            gap: 8px;
            transition: all 0.12s ease;
        }

        .btn-secondary:hover {
            background: var(--accent);
            color: #ffffff;
        }

        /* Status messages */
        .status {
            margin-top: 20px;
            padding: 16px;
            border-radius: 12px;
            text-align: center;
            font-weight: 500;
        }

        .status.success {
            background: #d1fae5;
            color: #065f46;
        }

        .status.error {
            background: #fee2e2;
            color: #991b1b;
        }

        .status.info {
            background: #dbeafe;
            color: #1e40af;
        }

        .status.loading {
            background: #fef3c7;
            color: #92400e;
        }

        /* Analysis results */
        .analysis-results {
            display: none;
            margin-top: 32px;
        }

        .analysis-results.show {
            display: block;
        }

        .result-card {
            background: rgba(255, 255, 255, 0.9);
            border-radius: 16px;
            padding: 20px;
            margin-bottom: 16px;
            border: 1px solid rgba(226, 232, 240, 0.8);
        }

        .result-card h3 {
            margin-bottom: 12px;
            color: var(--accent);
            display: flex;
            align-items: center;
            gap: 8px;
        }

        .result-card h3 .card-icon {
            width: 20px;
            height: 20px;
        }

        .inline-icon {
            width: 16px;
            height: 16px;
            margin-right: 8px;
            vertical-align: middle;
        }

        .status-icon {
            width: 16px;
            height: 16px;
            margin-right: 8px;
            vertical-align: middle;
        }

        .result-card p {
            margin-bottom: 8px;
            color: var(--text-muted);
        }

        .tag {
            display: inline-block;
            padding: 4px 8px;
            background: var(--accent-soft);
            color: var(--accent);
            border-radius: 999px;
            font-size: 12px;
            font-weight: 500;
            margin-right: 8px;
            margin-bottom: 8px;
        }

        /* Tab content */
        .tab-content {
            display: none;
        }

        .tab-content.active {
            display: block;
        }

        .btn-primary .btn-icon,
        .btn-secondary .btn-icon {
            width: 16px;
            height: 16px;
        }

        .spinning {
            animation: spin 1s linear infinite;
        }

        @keyframes spin {
            from { transform: rotate(0deg); }
            to { transform: rotate(360deg); }
        }

        .header-icon {
            width: 24px;
            height: 24px;
            margin-right: 8px;
        }

        @media (max-width: 720px) {
            .tabs {
                width: 100%;
                justify-content: space-between;
            }
            .tab {
                flex: 1;
                justify-content: center;
                padding-inline: 10px;
            }
            .actions {
                flex-direction: column;
            }
        }
    </style>
</head>
<body>
    <div class="page">
        <header class="header">
            <div class="brand">
                <div class="brand-logo">
                    <i data-lucide="rocket" class="logo-icon"></i>
                </div>
                <div>
                    <div class="brand-text-title">SensCoder MCP</div>
                    <div class="brand-text-sub">AI-Powered Project Setup</div>
                </div>
            </div>
        </header>

        <div class="tabs">
            <button class="tab active" onclick="switchTab('auto')">
                <i data-lucide="bot" class="icon"></i>
                <span>Auto Setup</span>
            </button>
            <button class="tab" onclick="switchTab('manual')">
                <i data-lucide="settings" class="icon"></i>
                <span>Manual Setup</span>
            </button>
        </div>

        <main class="main">
            <div class="content">
                <!-- Auto Setup Tab -->
                <div id="auto" class="tab-content active">
                    <section class="card">
                        <header class="card-header">
                            <h1><i data-lucide="zap" class="header-icon"></i> One-Click Project Setup</h1>
                            <p>Select your project folder and let AI analyze everything automatically</p>
                        </header>

                        <div class="form-group">
                            <label for="autoProjectPath">Project Folder Path</label>
                            <input type="text" id="autoProjectPath" placeholder="C:\\path\\to\\your\\project or /home/user/project" required>
                            <small style="color: var(--text-muted); font-size: 14px;">Enter the absolute path to your project directory</small>
                        </div>

                        <div class="actions">
                            <button class="btn-primary" onclick="runAutoSetup()">
                                <i data-lucide="zap" class="btn-icon"></i>
                                Auto-Generate Setup
                            </button>
                        </div>

                        <div id="autoStatus" class="status" style="display: none;"></div>

                        <div id="analysisResults" class="analysis-results">
                            <div class="result-card">
                                <h3><i data-lucide="search" class="card-icon"></i> Project Analysis</h3>
                                <div id="projectInfo"></div>
                            </div>

                            <div class="result-card">
                                <h3><i data-lucide="file-text" class="card-icon"></i> Generated Documentation</h3>
                                <p><i data-lucide="check-circle" class="inline-icon"></i> Product Requirements Document (PRD)</p>
                                <p><i data-lucide="check-circle" class="inline-icon"></i> Feature List & Technical Summary</p>
                                <p><i data-lucide="check-circle" class="inline-icon"></i> Health Report & Improvements</p>
                                <p><i data-lucide="check-circle" class="inline-icon"></i> Testing Plan & Codebase Summary</p>
                            </div>

                            <div class="actions">
                                <button class="btn-secondary" onclick="downloadReport()">
                                    <i data-lucide="download" class="btn-icon"></i>
                                    Download Full Report
                                </button>
                                <button class="btn-primary" onclick="proceedToMCP()">
                                    <i data-lucide="check" class="btn-icon"></i>
                                    Proceed to MCP
                                </button>
                            </div>
                        </div>
                    </section>
                </div>

                <!-- Manual Setup Tab -->
                <div id="manual" class="tab-content">
                    <section class="card">
                        <header class="card-header">
                            <h1><i data-lucide="settings" class="header-icon"></i> Manual Project Setup</h1>
                            <p>Configure your project settings manually</p>
                        </header>

                        <form id="manualSetupForm">
                            <div class="form-group">
                                <label for="manualProjectRoot">Project Folder Path</label>
                                <input type="text" id="manualProjectRoot" name="projectRoot" placeholder="C:\\path\\to\\your\\project" required>
                            </div>

                            <div class="form-group">
                                <label for="manualProjectType">Project Type</label>
                                <select id="manualProjectType" name="projectType" required>
                                    <option value="">Select project type...</option>
                                    <option value="nextjs">Next.js</option>
                                    <option value="vite">Vite</option>
                                    <option value="node">Node.js</option>
                                    <option value="python">Python</option>
                                    <option value="react">React</option>
                                    <option value="flask">Flask</option>
                                    <option value="django">Django</option>
                                    <option value="spring">Spring Boot</option>
                                    <option value="go">Go</option>
                                    <option value="other">Other</option>
                                </select>
                            </div>

                            <div class="actions">
                                <button type="submit" class="btn-primary">
                                    <i data-lucide="save" class="btn-icon"></i>
                                    Save Configuration
                                </button>
                            </div>
                        </form>

                        <div id="manualStatus" class="status" style="display: none;"></div>
                    </section>
                </div>
            </div>
        </main>
    </div>

    <script>
        let analysisData = null;

        function switchTab(tabName) {
            // Hide all tabs
            document.querySelectorAll('.tab-content').forEach(content => {
                content.classList.remove('active');
            });
            document.querySelectorAll('.tab').forEach(tab => {
                tab.classList.remove('active');
            });

            // Show selected tab
            document.getElementById(tabName).classList.add('active');
            event.target.classList.add('active');
        }

        function showStatus(message, type = 'info', containerId = 'autoStatus') {
            const status = document.getElementById(containerId);
            status.textContent = message;
            status.className = `status ${type}`;
            status.style.display = 'block';
        }

        function hideStatus(containerId = 'autoStatus') {
            document.getElementById(containerId).style.display = 'none';
        }

        async function runAutoSetup() {
            const projectPath = document.getElementById('autoProjectPath').value.trim();
            if (!projectPath) {
                showStatus('Please enter a project path', 'error');
                return;
            }

            const btn = event.target;
            btn.disabled = true;
            btn.innerHTML = '<i data-lucide="loader" class="btn-icon spinning"></i> Analyzing...';
            hideStatus();

            try {
                showStatus('🔍 Analyzing project structure...', 'loading');

                // Step 1: Analyze project
                const analysisResponse = await fetch('/mcp/analyze-project', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ projectPath })
                });

                if (!analysisResponse.ok) {
                    throw new Error('Project analysis failed');
                }

                const analysis = await analysisResponse.json();
                showStatus('<i data-lucide="clipboard-list" class="status-icon"></i> Generating documentation...', 'loading');

                // Step 2: Run auto-setup
                const setupResponse = await fetch('/mcp/auto-setup', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ projectPath })
                });

                if (!setupResponse.ok) {
                    throw new Error('Auto-setup failed');
                }

                const result = await setupResponse.json();
                analysisData = result;

                // Display results
                displayAnalysisResults(result);
                document.getElementById('analysisResults').classList.add('show');

                showStatus('<i data-lucide="check-circle" class="status-icon"></i> Setup completed successfully! Proceeding to MCP...', 'success');

                btn.disabled = false;
                btn.innerHTML = '<i data-lucide="zap" class="btn-icon"></i> Auto-Generate Setup';

                // Automatically proceed to MCP after showing results for 3 seconds
                setTimeout(() => {
                    proceedToMCP();
                }, 3000);

            } catch (error) {
                showStatus(`<i data-lucide="alert-circle" class="status-icon"></i> Error: ${error.message}`, 'error');
                btn.disabled = false;
                btn.innerHTML = '<i data-lucide="zap" class="btn-icon"></i> Auto-Generate Setup';
            }
        }

        function displayAnalysisResults(data) {
            const projectInfo = document.getElementById('projectInfo');

            const metadata = data.project_metadata;
            const languages = metadata.languages.map(lang => `<span class="tag">${lang}</span>`).join('');
            const frameworks = metadata.frameworks.map(fw => `<span class="tag">${fw}</span>`).join('');

            projectInfo.innerHTML = `
                <p><strong>Type:</strong> ${metadata.project_type}</p>
                <p><strong>Languages:</strong> ${languages || 'None detected'}</p>
                <p><strong>Frameworks:</strong> ${frameworks || 'None detected'}</p>
                <p><strong>Tests:</strong> ${metadata.has_tests ? '<i data-lucide="check-circle" class="inline-icon"></i> Detected' : '<i data-lucide="x-circle" class="inline-icon"></i> Not found'}</p>
                <p><strong>Health Score:</strong> ${metadata.health_score}/100</p>
                <p><strong>Entry Points:</strong> ${metadata.entry_points.join(', ') || 'None found'}</p>
            `;
        }

        function downloadReport() {
            if (!analysisData) return;

            const report = JSON.stringify(analysisData, null, 2);
            const blob = new Blob([report], { type: 'application/json' });
            const url = URL.createObjectURL(blob);

            const a = document.createElement('a');
            a.href = url;
            a.download = 'project-analysis-report.json';
            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a);
            URL.revokeObjectURL(url);
        }

        function proceedToMCP() {
            if (!analysisData) {
                window.location.href = '/';
                return;
            }

            // Save documentation files first
            saveDocumentation().then(() => {
                window.location.href = '/';
            }).catch((error) => {
                console.error('Failed to save documentation:', error);
                // Still proceed to MCP even if saving fails
                window.location.href = '/';
            });
        }

        async function saveDocumentation() {
            if (!analysisData) return;

            const projectPath = document.getElementById('autoProjectPath').value.trim();
            if (!projectPath) return;

            try {
                const response = await fetch('/mcp/save-documentation', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        projectPath: projectPath,
                        documentation: analysisData.documentation
                    })
                });

                if (!response.ok) {
                    throw new Error('Failed to save documentation');
                }

                console.log('Documentation saved successfully');
            } catch (error) {
                console.error('Error saving documentation:', error);
                throw error;
            }
        }

        // Manual setup form handler
        document.getElementById('manualSetupForm').addEventListener('submit', async (e) => {
            e.preventDefault();

            const submitBtn = e.target.querySelector('button[type="submit"]');
            submitBtn.disabled = true;
            submitBtn.innerHTML = '<i data-lucide="save" class="btn-icon"></i> Saving...';
            hideStatus('manualStatus');

            try {
                const formData = new FormData(e.target);
                const data = {};

                for (let [key, value] of formData.entries()) {
                    if (value.trim()) {
                        if (key === 'port') {
                            data[key] = parseInt(value);
                        } else {
                            data[key] = value;
                        }
                    }
                }

                const response = await fetch('/wizard/setup', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(data)
                });

                const result = await response.json();

                if (response.ok) {
                    showStatus('Project configured successfully!', 'success', 'manualStatus');
                    submitBtn.innerHTML = '<i data-lucide="check-circle" class="btn-icon"></i> Setup Complete';
                    setTimeout(() => {
                        window.location.href = '/';
                    }, 2000);
                } else {
                    throw new Error(result.detail || 'Setup failed');
                }

            } catch (error) {
                showStatus(error.message, 'error', 'manualStatus');
                submitBtn.disabled = false;
                submitBtn.innerHTML = '<i data-lucide="save" class="btn-icon"></i> Save Configuration';
            }
        });

        // Auto-detect project type for manual setup
        document.getElementById('manualProjectRoot').addEventListener('blur', async (e) => {
            const path = e.target.value;
            if (!path) return;

            try {
                const response = await fetch('/wizard/detect-type', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ path })
                });

                if (response.ok) {
                    const result = await response.json();
                    if (result.projectType) {
                        document.getElementById('manualProjectType').value = result.projectType;
                    }
                }
            } catch (error) {
                // Ignore detection errors
            }
        });

        // Initialize Lucide icons
        document.addEventListener('DOMContentLoaded', () => {
            lucide.createIcons();
        });
    </script>
</body>
</html>
"""

# Write the template to file
with open(templates_dir / "wizard.html", "w", encoding="utf-8") as f:
    f.write(wizard_html)


@router.get("/wizard", response_class=HTMLResponse)
async def wizard_page(request: Request):
    """Serve the project setup wizard page."""
    return templates.TemplateResponse("wizard.html", {"request": request})


@router.post("/wizard/setup")
async def setup_project(request: Request):
    """Setup project configuration."""
    try:
        data = await request.json()

        # Validate project config
        config = ProjectConfig(**data)
        project_manager.set_project_config(config)

        return {"message": "Project configured successfully", "config": config.dict()}

    except ValidationError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Setup failed: {str(e)}")


@router.post("/wizard/detect-type")
async def detect_project_type(request: Request):
    """Auto-detect project type based on files in the directory."""
    try:
        data = await request.json()
        path = data.get("path", "").strip()

        if not path or not os.path.exists(path):
            return {"projectType": None}

        # Check for common project files
        files = os.listdir(path)

        if "package.json" in files:
            with open(os.path.join(path, "package.json"), "r") as f:
                try:
                    package_data = json.load(f)
                    dependencies = package_data.get("dependencies", {})

                    if "next" in dependencies:
                        return {"projectType": "nextjs"}
                    elif "vite" in dependencies:
                        return {"projectType": "vite"}
                    else:
                        return {"projectType": "node"}
                except:
                    return {"projectType": "node"}

        elif "requirements.txt" in files or "pyproject.toml" in files or "setup.py" in files:
            return {"projectType": "python"}

        elif "Cargo.toml" in files:
            return {"projectType": "rust"}

        elif "go.mod" in files:
            return {"projectType": "go"}

        return {"projectType": "other"}

    except Exception as e:
        return {"projectType": None, "error": str(e)}


@router.get("/wizard/status")
async def get_wizard_status():
    """Get current wizard/project status."""
    config = project_manager.get_project_config()
    return {
        "configured": project_manager.is_configured(),
        "project_root": config.project_root if config else None,
        "project_type": config.project_type if config else None,
    }