"""Git service for safe git operations within project boundaries."""
import re
from typing import Dict, List, Optional, Any

from app.config import settings
from app.project_manager import project_manager
from app.utils.subprocess_utils import run_command_sync, DangerousCommandError


class GitService:
    """Service for safe git operations within project boundaries."""

    ALLOWED_SUBCOMMANDS = {'status', 'log', 'diff', 'branch', 'remote'}

    async def execute_git_command(
        self,
        subcommand: str,
        args: List[str],
        user_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Execute a git command safely within the project directory.

        Args:
            subcommand: Git subcommand (status, log, diff, etc.)
            args: Additional git arguments
            user_id: User ID for context

        Returns:
            Dict with git command results

        Raises:
            ValueError: If git is not allowed or subcommand is invalid
        """
        # Check if git operations are allowed
        if not settings.senscoder_allow_git:
            raise ValueError("Git operations are disabled in server configuration")

        # Validate subcommand
        if subcommand not in self.ALLOWED_SUBCOMMANDS:
            raise ValueError(f"Unsupported git subcommand: {subcommand}")

        # Get project root from project manager
        config = project_manager.get_project_config()
        if not config:
            raise ValueError("Project not configured. Please run the wizard at /wizard to set up your project.")

        project_root = config.project_root

        # Build git command
        git_args = [subcommand] + args

        # Execute git command
        try:
            stdout, stderr, exit_code = run_command_sync(
                'git',
                git_args,
                cwd=str(project_root),
                timeout=30
            )

            # Format response based on subcommand
            if subcommand == 'status':
                return {
                    'status': stdout.strip(),
                    'has_changes': exit_code != 0 or 'nothing to commit' not in stdout.lower()
                }
            elif subcommand == 'log':
                # Parse log output into structured format
                return self._parse_git_log(stdout)
            elif subcommand == 'diff':
                return {
                    'diff': stdout,
                    'has_changes': bool(stdout.strip())
                }
            elif subcommand == 'branch':
                return self._parse_git_branch(stdout)
            elif subcommand == 'remote':
                return self._parse_git_remote(stdout)
            else:
                return {
                    'output': stdout,
                    'error': stderr,
                    'exit_code': exit_code
                }

        except DangerousCommandError as e:
            raise ValueError(f"Git command blocked for safety: {e}")
        except TimeoutError:
            raise ValueError("Git command execution timed out")
        except FileNotFoundError:
            raise ValueError("Git command not found - ensure git is installed")
        except Exception as e:
            raise ValueError(f"Git command execution failed: {e}")

    def _parse_git_log(self, log_output: str) -> Dict[str, Any]:
        """Parse git log output into structured format."""
        commits = []
        lines = log_output.strip().split('\n')

        for line in lines:
            line = line.strip()
            if not line:
                continue

            # Simple commit parsing - can be enhanced
            if line.startswith('commit '):
                commit_hash = line.split()[1]
                commits.append({'hash': commit_hash, 'full': line})
            else:
                if commits:
                    commits[-1]['full'] += '\n' + line

        return {
            'commits': commits,
            'count': len(commits)
        }

    def _parse_git_branch(self, branch_output: str) -> Dict[str, Any]:
        """Parse git branch output."""
        branches = []
        current_branch = None

        for line in branch_output.strip().split('\n'):
            line = line.strip()
            if line.startswith('*'):
                current_branch = line[1:].strip()
                branches.append(line[1:].strip())
            else:
                branches.append(line)

        return {
            'branches': branches,
            'current': current_branch
        }

    def _parse_git_remote(self, remote_output: str) -> Dict[str, Any]:
        """Parse git remote output."""
        remotes = []
        for line in remote_output.strip().split('\n'):
            if line.strip():
                parts = line.split()
                if len(parts) >= 2:
                    remotes.append({
                        'name': parts[0],
                        'url': parts[1]
                    })

        return {'remotes': remotes}


# Global service instance
git_service = GitService()