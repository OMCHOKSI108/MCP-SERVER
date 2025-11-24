"""Pydantic models for MCP server requests and responses."""
from typing import Any, Dict, List, Optional, Union

from pydantic import BaseModel, Field


# Tool invocation models
class ToolInvokeRequest(BaseModel):
    """Request model for tool invocation."""
    tool: str = Field(..., min_length=1, max_length=50, pattern=r'^[a-zA-Z_][a-zA-Z0-9_]*$', description="Name of the tool to invoke")
    params: Dict[str, Any] = Field(default_factory=dict, description="Tool parameters")
    user_id: Optional[str] = Field(None, min_length=1, max_length=100, description="User ID for context")

    class Config:
        extra = "forbid"  # Prevent extra fields


class ToolInvokeResponse(BaseModel):
    """Response model for tool invocation."""
    ok: bool = Field(..., description="Whether the tool invocation was successful")
    tool: str = Field(..., description="Name of the invoked tool")
    result: Optional[Dict[str, Any]] = Field(None, description="Tool execution result")
    error: Optional[str] = Field(None, description="Error message if ok=False")


# Resource models
class ResourceData(BaseModel):
    """Data structure for a resource."""
    id: str = Field(..., description="Unique resource identifier")
    name: str = Field(..., description="Human-readable resource name")
    description: str = Field(..., description="Resource description")
    data: Dict[str, Any] = Field(..., description="Resource content/data")


class ResourceResponse(BaseModel):
    """Response model for resources endpoint."""
    resources: List[ResourceData] = Field(..., description="List of available resources")


# Prompt models
class PromptTemplate(BaseModel):
    """Template structure for a prompt."""
    id: str = Field(..., description="Unique prompt identifier")
    title: str = Field(..., description="Human-readable prompt title")
    description: str = Field(..., description="Prompt description")
    template: str = Field(..., description="Prompt template content")


class PromptsResponse(BaseModel):
    """Response model for prompts endpoint."""
    prompts: List[PromptTemplate] = Field(..., description="List of available prompts")


# Tool-specific parameter models
class EchoParams(BaseModel):
    """Parameters for echo tool."""
    text: str = Field(..., min_length=1, max_length=1000, description="Text to echo back")

    class Config:
        extra = "forbid"


class MathParams(BaseModel):
    """Parameters for math tool."""
    expression: str = Field(..., min_length=1, max_length=200, description="Mathematical expression to evaluate")

    class Config:
        extra = "forbid"


class ReadFileParams(BaseModel):
    """Parameters for read_file tool."""
    path: str = Field(..., min_length=1, max_length=500, description="Relative path to file within project root")

    class Config:
        extra = "forbid"


class WriteFileParams(BaseModel):
    """Parameters for write_file tool."""
    path: str = Field(..., min_length=1, max_length=500, description="Relative path to file within project root")
    content: str = Field(..., min_length=0, max_length=100000, description="Content to write to the file")

    class Config:
        extra = "forbid"


class ListFilesParams(BaseModel):
    """Parameters for list_files tool."""
    path: Optional[str] = Field(".", min_length=0, max_length=500, description="Relative path to directory within project root")

    class Config:
        extra = "forbid"


class ExecParams(BaseModel):
    """Parameters for exec tool."""
    command: str = Field(..., min_length=1, max_length=100, description="Command to execute")
    args: List[str] = Field(default_factory=list, max_items=10, description="Command arguments")

    class Config:
        extra = "forbid"


class GitParams(BaseModel):
    """Parameters for git tool."""
    subcommand: str = Field(..., min_length=1, max_length=50, description="Git subcommand (status, log, diff)")
    args: List[str] = Field(default_factory=list, max_items=10, description="Additional git arguments")

    class Config:
        extra = "forbid"


class GetProviderConfigParams(BaseModel):
    """Parameters for get_provider_config tool."""
    user_id: str = Field(..., min_length=1, max_length=100, description="User ID to get config for")

    class Config:
        extra = "forbid"


# Tool result models
class FileEntry(BaseModel):
    """File/directory entry for list_files results."""
    name: str = Field(..., description="Entry name")
    path: str = Field(..., description="Relative path")
    is_dir: bool = Field(..., description="Whether this is a directory")
    size: Optional[int] = Field(None, description="File size in bytes")


class ExecResult(BaseModel):
    """Result of exec command execution."""
    stdout: str = Field(..., description="Standard output")
    stderr: str = Field(..., description="Standard error")
    exit_code: int = Field(..., description="Process exit code")


class ProviderConfig(BaseModel):
    """Provider configuration from backend."""
    provider: str = Field(..., description="AI provider name")
    use_own_key: bool = Field(..., description="Whether user uses their own API key")
    has_api_key: bool = Field(..., description="Whether API key is configured")


# Error models
class ErrorResponse(BaseModel):
    """Generic error response."""
    error: str = Field(..., description="Error message")
    details: Optional[Dict[str, Any]] = Field(None, description="Additional error details")