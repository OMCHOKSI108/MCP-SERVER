"""Safe subprocess utilities for command execution."""
import asyncio
import shlex
from typing import List, Optional, Tuple

from app.config import settings


class DangerousCommandError(Exception):
    """Raised when a potentially dangerous command is detected."""
    pass


def validate_command_safety(command: str, args: List[str]) -> None:
    """
    Validate that a command is safe to execute.

    Args:
        command: The command to validate
        args: Command arguments

    Raises:
        DangerousCommandError: If command is deemed dangerous
    """
    dangerous_commands = {
        'rm', 'del', 'delete', 'format', 'fdisk', 'mkfs',
        'dd', 'shred', 'wipe', 'sdelete', 'cipher'
    }

    dangerous_patterns = [
        'rm -rf /', 'del /', 'format c:', 'fdisk', 'mkfs',
        'dd if=', 'shred', '> /dev/null', '> nul'
    ]

    # Check command name
    if command.lower() in dangerous_commands:
        # Allow some safe rm usage
        if command.lower() == 'rm':
            args_str = ' '.join(args)
            if '-rf' in args or '--force' in args:
                if '/' in args_str or '/*' in args_str:
                    raise DangerousCommandError(f"Dangerous rm command: {command} {' '.join(args)}")
        else:
            raise DangerousCommandError(f"Dangerous command: {command}")

    # Check for dangerous patterns
    full_command = f"{command} {' '.join(args)}"
    for pattern in dangerous_patterns:
        if pattern in full_command.lower():
            raise DangerousCommandError(f"Dangerous command pattern detected: {pattern}")


async def run_command_async(
    command: str,
    args: List[str],
    cwd: Optional[str] = None,
    timeout: int = 30
) -> Tuple[str, str, int]:
    """
    Run a command asynchronously with safety checks.

    Args:
        command: Command to run
        args: Command arguments
        cwd: Working directory
        timeout: Command timeout in seconds

    Returns:
        Tuple of (stdout, stderr, exit_code)

    Raises:
        DangerousCommandError: If command is unsafe
        asyncio.TimeoutError: If command times out
    """
    # Validate command safety
    validate_command_safety(command, args)

    # Prepare the process
    process = await asyncio.create_subprocess_exec(
        command,
        *args,
        cwd=cwd or str(settings.project_root_path),
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )

    try:
        # Wait for completion with timeout
        stdout, stderr = await asyncio.wait_for(
            process.communicate(),
            timeout=timeout
        )

        # Decode output
        stdout_str = stdout.decode('utf-8', errors='replace')
        stderr_str = stderr.decode('utf-8', errors='replace')

        return stdout_str, stderr_str, process.returncode or 0

    except asyncio.TimeoutError:
        # Kill the process if it times out
        try:
            process.kill()
            await process.wait()
        except:
            pass
        raise asyncio.TimeoutError(f"Command timed out after {timeout} seconds")


def run_command_sync(
    command: str,
    args: List[str],
    cwd: Optional[str] = None,
    timeout: int = 30
) -> Tuple[str, str, int]:
    """
    Run a command synchronously with safety checks.

    Args:
        command: Command to run
        args: Command arguments
        cwd: Working directory
        timeout: Command timeout in seconds

    Returns:
        Tuple of (stdout, stderr, exit_code)
    """
    try:
        # Run in a new event loop
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        result = loop.run_until_complete(
            run_command_async(command, args, cwd, timeout)
        )
        loop.close()
        return result
    except asyncio.TimeoutError:
        raise TimeoutError(f"Command timed out after {timeout} seconds")