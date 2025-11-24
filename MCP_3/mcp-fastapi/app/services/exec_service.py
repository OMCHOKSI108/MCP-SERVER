"""Execution service for running shell commands safely."""
from typing import List, Optional

from app.config import settings
from app.models import ExecResult
from app.project_manager import project_manager
from app.utils.subprocess_utils import run_command_sync, DangerousCommandError


class ExecutionService:
    """Service for safe command execution within project boundaries."""

    async def execute_command(
        self,
        command: str,
        args: List[str],
        user_id: Optional[str] = None
    ) -> ExecResult:
        """
        Execute a command safely within the project directory.

        Args:
            command: Command to execute
            args: Command arguments
            user_id: User ID for context

        Returns:
            Execution result with stdout, stderr, and exit code

        Raises:
            ValueError: If exec is not allowed or command is invalid
            DangerousCommandError: If command is deemed dangerous
        """
        # Check if execution is allowed
        if not settings.senscoder_allow_exec:
            raise ValueError("Command execution is disabled in server configuration")

        # Validate command
        if not command or not command.strip():
            raise ValueError("Command cannot be empty")

        # Get project root from project manager
        config = project_manager.get_project_config()
        if not config:
            raise ValueError("Project not configured. Please run the wizard at /wizard to set up your project.")

        project_root = config.project_root

        # Execute command in project root
        try:
            stdout, stderr, exit_code = run_command_sync(
                command,
                args,
                cwd=str(project_root),
                timeout=30  # 30 second timeout
            )

            return ExecResult(
                stdout=stdout,
                stderr=stderr,
                exit_code=exit_code
            )

        except DangerousCommandError as e:
            raise ValueError(f"Command blocked for safety: {e}")
        except TimeoutError:
            raise ValueError("Command execution timed out")
        except FileNotFoundError:
            raise ValueError(f"Command not found: {command}")
        except Exception as e:
            raise ValueError(f"Command execution failed: {e}")


# Global service instance
exec_service = ExecutionService()