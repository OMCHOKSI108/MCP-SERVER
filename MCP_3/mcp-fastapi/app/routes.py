"""FastAPI routes for MCP server endpoints."""
from typing import List, Dict, Any, Optional
from pathlib import Path

from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import StreamingResponse

from app.models import (
    ToolInvokeRequest, ToolInvokeResponse,
    ResourceData, PromptTemplate,
    ResourceResponse, PromptsResponse
)
from app.mcp_server import mcp_server
from app.config import settings
from app.auth import get_current_user, get_optional_user, AuthService
from app.services.project_analyzer import project_analyzer, ProjectMetadata
from app.services.documentation_generator import documentation_generator

router = APIRouter(prefix="/mcp", tags=["mcp"])


# Health check endpoint
@router.get("/health")
async def health_check() -> Dict[str, Any]:
    """
    Health check endpoint for MCP server.

    Returns server status and capabilities.
    """
    try:
        # Get server capabilities
        tools_count = len(mcp_server.tools) if hasattr(mcp_server, 'tools') else 0
        resources_count = len(mcp_server.get_resources().resources) if hasattr(mcp_server, 'get_resources') else 0
        prompts_count = len(mcp_server.get_prompts().prompts) if hasattr(mcp_server, 'get_prompts') else 0

        return {
            "status": "healthy",
            "server": "SensCoder MCP",
            "version": "0.1.0",
            "tools_count": tools_count,
            "resources_count": resources_count,
            "prompts_count": prompts_count
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "error": str(e)
        }


# Authentication endpoints
@router.post("/auth/login")
async def login(request: dict):
    """
    Generate JWT token for MCP access.

    In production, this should validate credentials against the backend.
    For now, accepts any user_id for testing.
    """
    user_id = request.get("user_id")
    if not user_id or not user_id.strip():
        raise HTTPException(status_code=400, detail="User ID is required")

    # In production, validate against backend here
    token = AuthService.create_access_token({"sub": user_id})
    return {"access_token": token, "token_type": "bearer"}


@router.post("/tool-invoke", response_model=ToolInvokeResponse)
async def invoke_tool(
    request: ToolInvokeRequest,
    current_user: dict = Depends(get_current_user)
) -> ToolInvokeResponse:
    """
    Invoke an MCP tool.

    This endpoint allows clients to invoke various tools provided by the MCP server,
    such as file operations, command execution, git operations, etc.
    """
    # Additional validation
    if not request.tool or not request.tool.strip():
        raise HTTPException(status_code=400, detail="Tool name is required")

    if len(request.tool) > 50:  # Reasonable limit
        raise HTTPException(status_code=400, detail="Tool name too long")

    # Set user_id from authenticated user if not provided
    if not request.user_id:
        request.user_id = current_user.get("sub")

    try:
        result = await mcp_server.invoke_tool(request)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Tool invocation failed: {str(e)}")


@router.get("/resources", response_model=ResourceResponse)
async def get_resources() -> ResourceResponse:
    """
    Get available MCP resources.

    Returns a list of resources that provide information about the MCP server
    and its capabilities.
    """
    try:
        resources = mcp_server.get_resources()
        return ResourceResponse(resources=resources)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get resources: {str(e)}")


@router.get("/prompts", response_model=PromptsResponse)
async def get_prompts() -> PromptsResponse:
    """
    Get available MCP prompts.

    Returns a list of prompt templates that can be used to guide AI assistants
    in various coding tasks.
    """
    try:
        prompts = mcp_server.get_prompts()
        return PromptsResponse(prompts=prompts)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get prompts: {str(e)}")


# Optional streaming endpoint for long-running operations
@router.post("/tool-invoke/stream")
async def invoke_tool_streaming(request: ToolInvokeRequest):
    """
    Invoke an MCP tool with streaming response.

    For long-running tools, this endpoint can stream results as they become available.
    Currently returns the same response as the regular endpoint.
    """
    try:
        result = await mcp_server.invoke_tool(request)

        # For now, return as regular JSON response
        # In the future, this could return a StreamingResponse for real-time updates
        return result

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Tool invocation failed: {str(e)}")


# Auto-setup endpoints for automatic project analysis and documentation generation
@router.post("/auto-setup")
async def auto_setup_project(
    request: Dict[str, Any],
    current_user: Optional[dict] = Depends(get_optional_user)
) -> Dict[str, Any]:
    """
    Automatically analyze project and generate all documentation.

    This endpoint performs complete project analysis and generates:
    - PRD (Product Requirements Document)
    - Feature list
    - Technical summary
    - Health report
    - Improvement recommendations
    - Testing plan
    - Codebase summary

    Expects: {"projectPath": "/path/to/project"}
    """
    try:
        project_path = request.get("projectPath", "").strip()
        if not project_path:
            raise HTTPException(status_code=400, detail="projectPath is required")

        user_id = current_user.get("sub") if current_user else settings.senscoder_default_user_id or "wizard-user"

        # Step 1: Analyze project
        print(f"Analyzing project at: {project_path}")
        metadata = project_analyzer.analyze_project(project_path)

        # Step 2: Generate all documentation
        print("Generating documentation...")
        prd = await documentation_generator.generate_prd(metadata, user_id)
        features = await documentation_generator.generate_feature_list(metadata, user_id)
        tech_summary = await documentation_generator.generate_tech_summary(metadata, user_id)
        health_report = await documentation_generator.generate_health_report(metadata, user_id)
        improvements = await documentation_generator.generate_improvements(metadata, user_id)
        testing_plan = await documentation_generator.generate_testing_plan(metadata, user_id)
        codebase_summary = await documentation_generator.generate_codebase_summary(metadata, user_id)

        # Step 3: Return comprehensive results
        result = {
            "success": True,
            "project_metadata": {
                "project_type": metadata.project_type.value,
                "languages": list(metadata.languages),
                "frameworks": list(metadata.frameworks),
                "has_tests": metadata.has_tests,
                "health_score": metadata.health_score,
                "entry_points": metadata.entry_points
            },
            "documentation": {
                "prd": prd,
                "features": features,
                "tech_summary": tech_summary,
                "health_report": health_report,
                "improvements": improvements,
                "testing_plan": testing_plan,
                "codebase_summary": codebase_summary
            },
            "generated_at": prd["generated_at"]  # All docs have same timestamp
        }

        print(f"Auto-setup completed for project: {project_path}")
        return result

    except Exception as e:
        print(f"Auto-setup failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Auto-setup failed: {str(e)}")


@router.post("/analyze-project")
async def analyze_project(
    request: Dict[str, Any],
    current_user: Optional[dict] = Depends(get_optional_user)
) -> Dict[str, Any]:
    """
    Analyze project structure and metadata.

    Returns detailed project analysis including:
    - Project type detection
    - Languages and frameworks
    - Dependencies
    - Build/test commands
    - Folder structure
    - Health metrics

    Expects: {"projectPath": "/path/to/project"}
    """
    try:
        project_path = request.get("projectPath", "").strip()
        if not project_path:
            raise HTTPException(status_code=400, detail="projectPath is required")

        print(f"Analyzing project at: {project_path}")
        metadata = project_analyzer.analyze_project(project_path)

        # Convert metadata to dict for JSON response
        result = {
            "project_type": metadata.project_type.value,
            "languages": list(metadata.languages),
            "frameworks": list(metadata.frameworks),
            "dependencies": metadata.dependencies,
            "dev_dependencies": metadata.dev_dependencies,
            "build_commands": metadata.build_commands,
            "start_commands": metadata.start_commands,
            "test_commands": metadata.test_commands,
            "has_tests": metadata.has_tests,
            "test_frameworks": list(metadata.test_frameworks),
            "config_files": metadata.config_files,
            "entry_points": metadata.entry_points,
            "package_managers": list(metadata.package_managers),
            "deployment_indicators": metadata.deployment_indicators,
            "vulnerabilities": metadata.vulnerabilities,
            "health_score": metadata.health_score,
            "folder_structure": metadata.folder_structure
        }

        return result

    except Exception as e:
        print(f"Project analysis failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")


@router.post("/generate-prd")
async def generate_prd(
    request: Dict[str, Any],
    current_user: Optional[dict] = Depends(get_optional_user)
) -> Dict[str, Any]:
    """
    Generate Product Requirements Document for a project.

    Expects: {"projectPath": "/path/to/project"}
    """
    try:
        project_path = request.get("projectPath", "").strip()
        if not project_path:
            raise HTTPException(status_code=400, detail="projectPath is required")

        user_id = current_user.get("sub") if current_user else settings.senscoder_default_user_id or "wizard-user"

        # Analyze project first
        metadata = project_analyzer.analyze_project(project_path)

        # Generate PRD
        prd = await documentation_generator.generate_prd(metadata, user_id)

        return prd

    except Exception as e:
        print(f"PRD generation failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"PRD generation failed: {str(e)}")


@router.post("/save-documentation")
async def save_documentation(
    request: Dict[str, Any],
    current_user: Optional[dict] = Depends(get_optional_user)
) -> Dict[str, Any]:
    """
    Save generated documentation to docs/ folder in the project.

    Expects: {"projectPath": "/path/to/project", "documentation": {...}}
    """
    try:
        project_path = request.get("projectPath", "").strip()
        documentation = request.get("documentation", {})

        if not project_path:
            raise HTTPException(status_code=400, detail="projectPath is required")

        if not documentation:
            raise HTTPException(status_code=400, detail="documentation is required")

        # Create docs directory
        docs_dir = Path(project_path) / "docs"
        docs_dir.mkdir(exist_ok=True)

        saved_files = []

        # Save each documentation piece
        doc_files = {
            "prd.md": documentation.get("prd", {}),
            "features.md": documentation.get("features", {}),
            "tech-summary.md": documentation.get("tech_summary", {}),
            "health-report.md": documentation.get("health_report", {}),
            "improvements.md": documentation.get("improvements", {}),
            "testing-plan.md": documentation.get("testing_plan", {}),
            "codebase-summary.md": documentation.get("codebase_summary", {})
        }

        for filename, content in doc_files.items():
            if content and isinstance(content, dict):
                # Convert dict to markdown
                markdown_content = dict_to_markdown(content)
                file_path = docs_dir / filename

                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(markdown_content)

                saved_files.append(str(file_path))

        return {
            "success": True,
            "saved_files": saved_files,
            "docs_directory": str(docs_dir)
        }

    except Exception as e:
        print(f"Save documentation failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Save documentation failed: {str(e)}")


def dict_to_markdown(data: Dict[str, Any]) -> str:
    """Convert documentation dict to markdown format."""
    lines = []

    # Title
    if "title" in data:
        lines.append(f"# {data['title']}")
        lines.append("")

    # Description
    if "description" in data:
        lines.append(data["description"])
        lines.append("")

    # Generated at
    if "generated_at" in data:
        lines.append(f"*Generated on: {data['generated_at']}*")
        lines.append("")

    # Content sections
    for key, value in data.items():
        if key in ["title", "description", "generated_at"]:
            continue

        if isinstance(value, str):
            lines.append(f"## {key.replace('_', ' ').title()}")
            lines.append("")
            lines.append(value)
            lines.append("")
        elif isinstance(value, list):
            lines.append(f"## {key.replace('_', ' ').title()}")
            lines.append("")
            for item in value:
                if isinstance(item, dict):
                    for sub_key, sub_value in item.items():
                        lines.append(f"- **{sub_key.replace('_', ' ').title()}:** {sub_value}")
                    lines.append("")
                else:
                    lines.append(f"- {item}")
            lines.append("")
        elif isinstance(value, dict):
            lines.append(f"## {key.replace('_', ' ').title()}")
            lines.append("")
            for sub_key, sub_value in value.items():
                if isinstance(sub_value, list):
                    lines.append(f"### {sub_key.replace('_', ' ').title()}")
                    for item in sub_value:
                        lines.append(f"- {item}")
                    lines.append("")
                else:
                    lines.append(f"**{sub_key.replace('_', ' ').title()}:** {sub_value}")
                    lines.append("")

    return "\n".join(lines)