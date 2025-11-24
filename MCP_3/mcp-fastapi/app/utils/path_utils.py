"""Path utilities for safe file operations within project root."""
import os
from pathlib import Path
from typing import Optional

from app.project_manager import project_manager


def resolve_safe_path(
    relative_path: str,
    user_id: Optional[str] = None,
    base_path: Optional[Path] = None
) -> Path:
    """
    Resolve a relative path safely within the project root.

    Args:
        relative_path: Relative path from project root
        user_id: User ID (reserved for future per-user project roots)
        base_path: Override base path (defaults to project root)

    Returns:
        Resolved absolute path within project boundaries

    Raises:
        ValueError: If path attempts to escape project root
    """
    if base_path is None:
        config = project_manager.get_project_config()
        if not config:
            raise ValueError("Project not configured. Please visit /wizard to set up your project.")
        base_path = config.project_path

    # Resolve the relative path
    requested_path = base_path / relative_path

    # Get the absolute, resolved path (handles .. and symlinks)
    resolved_path = requested_path.resolve()

    # Ensure the resolved path is still within the project root
    try:
        resolved_path.relative_to(base_path)
    except ValueError:
        raise ValueError(f"Path attempts to escape project root: {relative_path}")

    return resolved_path


def ensure_parent_directory(path: Path) -> None:
    """Ensure the parent directory of a path exists."""
    path.parent.mkdir(parents=True, exist_ok=True)


def is_text_file(path: Path) -> bool:
    """Check if a file is likely to be a text file based on extension."""
    text_extensions = {
        '.txt', '.md', '.py', '.js', '.ts', '.jsx', '.tsx', '.html', '.css',
        '.scss', '.sass', '.less', '.json', '.xml', '.yaml', '.yml', '.toml',
        '.ini', '.cfg', '.conf', '.sh', '.bash', '.zsh', '.fish', '.ps1',
        '.sql', '.csv', '.log', '.env', '.gitignore', '.dockerfile'
    }

    # Check file extension
    if path.suffix.lower() in text_extensions:
        return True

    # Check if file has no extension and is in common text locations
    if not path.suffix and path.name in {'README', 'LICENSE', 'CHANGELOG', 'Makefile'}:
        return True

    return False


def get_file_size_mb(path: Path) -> float:
    """Get file size in megabytes."""
    return path.stat().st_size / (1024 * 1024)