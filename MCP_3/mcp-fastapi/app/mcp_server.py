"""Core MCP server logic with tool registry and MCP functionality."""
import ast
import operator
from typing import Any, Dict, List, Callable, Optional

from app.models import (
    ResourceData, PromptTemplate, ProviderConfig,
    ToolInvokeRequest, ToolInvokeResponse
)
from app.services import fs_service, exec_service, git_service, config_service
from app.project_manager import project_manager


class MCPServer:
    """Core MCP server with tool registry and resource management."""

    def __init__(self):
        self.tools: Dict[str, Callable] = {}
        self.resources: List[ResourceData] = []
        self.prompts: List[PromptTemplate] = []
        self._register_tools()
        self._register_resources()
        self._register_prompts()

    def _register_tools(self):
        """Register all available MCP tools."""
        self.tools = {
            'echo': self._tool_echo,
            'math': self._tool_math,
            'read_file': self._tool_read_file,
            'write_file': self._tool_write_file,
            'list_files': self._tool_list_files,
            'exec': self._tool_exec,
            'git': self._tool_git,
            'get_provider_config': self._tool_get_provider_config,
            'open_wizard': self._tool_open_wizard,
        }

    def _register_resources(self):
        """Register available MCP resources."""
        self.resources = [
            ResourceData(
                id="senscoder:about",
                name="SensCoder MCP Info",
                description="Basic information about the SensCoder local MCP server.",
                data={
                    "name": "SensCoder MCP",
                    "version": "0.1.0",
                    "description": "Local-first coding assistant MCP server",
                    "langs": ["python", "node", "javascript", "typescript"],
                    "features": ["fs", "exec", "git", "config"],
                    "capabilities": ["tools", "resources", "prompts"]
                }
            )
        ]

    def _register_prompts(self):
        """Register available MCP prompts."""
        self.prompts = [
            PromptTemplate(
                id="code_review",
                title="Code Review Assistant",
                description="Instructions for reviewing code changes and providing feedback.",
                template="""
You are a senior software engineer conducting a code review. Review the following code for:

1. **Code Quality**: Readability, maintainability, and adherence to best practices
2. **Functionality**: Correctness and completeness of implementation
3. **Security**: Potential security vulnerabilities or unsafe practices
4. **Performance**: Efficiency and potential bottlenecks
5. **Testing**: Test coverage and test quality
6. **Documentation**: Code comments and documentation completeness

Code to review:
```
{code}
```

Please provide specific, actionable feedback with examples where appropriate.
"""
            ),
            PromptTemplate(
                id="add_tests",
                title="Generate Unit Tests",
                description="Instructions for generating comprehensive unit tests for code.",
                template="""
You are a QA engineer tasked with creating comprehensive unit tests. Generate tests for the following code:

Code to test:
```
{code}
```

Requirements:
1. **Test Coverage**: Cover all functions, methods, and edge cases
2. **Test Types**: Unit tests, integration tests where appropriate
3. **Frameworks**: Use appropriate testing frameworks (pytest for Python, Jest for JS, etc.)
4. **Mocking**: Mock external dependencies and side effects
5. **Edge Cases**: Test error conditions, boundary values, and unusual inputs
6. **Assertions**: Clear, descriptive assertions with helpful error messages

Generate complete, runnable test code with proper setup and teardown.
"""
            ),
            PromptTemplate(
                id="debug_issue",
                title="Debug Code Issue",
                description="Instructions for debugging and fixing code issues.",
                template="""
You are a debugging expert. Help resolve the following issue:

**Problem Description:**
{problem}

**Code Context:**
```
{code}
```

**Error Messages (if any):**
{errors}

**Steps to Debug:**
1. **Reproduce**: How to reproduce the issue
2. **Analyze**: Root cause analysis
3. **Fix**: Specific code changes needed
4. **Test**: How to verify the fix works
5. **Prevent**: How to prevent similar issues in the future

Provide a step-by-step debugging process and the final solution.
"""
            )
        ]

    async def invoke_tool(self, request: ToolInvokeRequest) -> ToolInvokeResponse:
        """
        Invoke an MCP tool.

        Args:
            request: Tool invocation request

        Returns:
            Tool invocation response
        """
        try:
            # Check if project is configured before allowing tool usage
            config = project_manager.get_project_config()
            if not config:
                return ToolInvokeResponse(
                    ok=False,
                    tool=request.tool,
                    error="Project not configured. Please visit http://localhost:8000/wizard to set up your project."
                )

            if request.tool not in self.tools:
                return ToolInvokeResponse(
                    ok=False,
                    tool=request.tool,
                    error=f"Unknown tool: {request.tool}"
                )

            tool_func = self.tools[request.tool]
            result = await tool_func(request.params, request.user_id)

            return ToolInvokeResponse(
                ok=True,
                tool=request.tool,
                result=result
            )

        except Exception as e:
            return ToolInvokeResponse(
                ok=False,
                tool=request.tool,
                error=str(e)
            )

    def get_resources(self) -> List[ResourceData]:
        """Get all available MCP resources."""
        return self.resources

    def get_prompts(self) -> List[PromptTemplate]:
        """Get all available MCP prompts."""
        return self.prompts

    # Tool implementations

    async def _tool_echo(self, params: Dict[str, Any], user_id: Optional[str]) -> Dict[str, Any]:
        """Echo tool - returns the input text."""
        text = params.get('text', '')
        return {'text': text}

    async def _tool_math(self, params: Dict[str, Any], user_id: Optional[str]) -> Dict[str, Any]:
        """Math tool - safely evaluates simple mathematical expressions."""
        expression = params.get('expression', '')

        if not expression:
            raise ValueError("Expression is required")

        # Validate expression contains only safe characters
        import re
        if not re.match(r'^[0-9+\-*/().\s]+$', expression):
            raise ValueError("Expression contains invalid characters")

        # Use AST to safely evaluate mathematical expressions
        try:
            # Parse the expression
            tree = ast.parse(expression, mode='eval')

            # Only allow safe operations
            allowed_names = {
                k: v for k, v in vars(operator).items()
                if not k.startswith('_') and callable(v)
            }
            allowed_names.update({
                'abs': abs, 'round': round, 'min': min, 'max': max,
                'sum': sum, 'len': len, 'pow': pow, 'sqrt': (lambda x: x ** 0.5)
            })

            # Evaluate with restricted globals
            result = eval(compile(tree, '<string>', 'eval'), {"__builtins__": {}}, allowed_names)

            return {'result': result}

        except (SyntaxError, NameError, TypeError, ZeroDivisionError) as e:
            raise ValueError(f"Invalid mathematical expression: {e}")

    async def _tool_read_file(self, params: Dict[str, Any], user_id: Optional[str]) -> Dict[str, Any]:
        """Read file tool."""
        path = params.get('path', '')
        if not path:
            raise ValueError("Path is required")

        return await fs_service.read_file(path, user_id)

    async def _tool_write_file(self, params: Dict[str, Any], user_id: Optional[str]) -> Dict[str, Any]:
        """Write file tool."""
        path = params.get('path', '')
        content = params.get('content', '')

        if not path:
            raise ValueError("Path is required")

        return await fs_service.write_file(path, content, user_id)

    async def _tool_list_files(self, params: Dict[str, Any], user_id: Optional[str]) -> Dict[str, Any]:
        """List files tool."""
        path = params.get('path', '.')
        entries = await fs_service.list_files(path, user_id)

        return {
            'entries': [entry.dict() for entry in entries],
            'count': len(entries)
        }

    async def _tool_exec(self, params: Dict[str, Any], user_id: Optional[str]) -> Dict[str, Any]:
        """Execute command tool."""
        command = params.get('command', '')
        args = params.get('args', [])

        if not command:
            raise ValueError("Command is required")

        result = await exec_service.execute_command(command, args, user_id)
        return result.dict()

    async def _tool_git(self, params: Dict[str, Any], user_id: Optional[str]) -> Dict[str, Any]:
        """Git command tool."""
        subcommand = params.get('subcommand', '')
        args = params.get('args', [])

        if not subcommand:
            raise ValueError("Git subcommand is required")

        return await git_service.execute_git_command(subcommand, args, user_id)

    async def _tool_get_provider_config(self, params: Dict[str, Any], user_id: Optional[str]) -> Dict[str, Any]:
        """Get provider config tool."""
        if not user_id:
            raise ValueError("User ID is required for provider config")

        config = await config_service.get_provider_config(user_id)
        return config.dict()

    async def _tool_open_wizard(self, params: Dict[str, Any], user_id: Optional[str]) -> Dict[str, Any]:
        """Open wizard tool - opens the project setup wizard in the default web browser."""
        import webbrowser
        import threading
        import time

        wizard_url = "http://localhost:8000/wizard"

        def open_browser():
            time.sleep(1)  # Give server a moment to start
            webbrowser.open(wizard_url)

        # Open browser in a separate thread
        threading.Thread(target=open_browser, daemon=True).start()

        return {
            'message': 'Opening project setup wizard...',
            'url': wizard_url,
            'instructions': 'The wizard should open in your default web browser. If it doesn\'t, manually navigate to the URL above.'
        }


# Global MCP server instance
mcp_server = MCPServer()