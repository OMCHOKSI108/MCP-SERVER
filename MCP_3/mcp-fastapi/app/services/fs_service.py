"""File system service for safe file operations."""
import os
from pathlib import Path
from typing import List, Optional

from app.config import settings
from app.models import FileEntry
from app.utils.path_utils import resolve_safe_path, is_text_file, get_file_size_mb


class FileSystemService:
    """Service for safe file system operations within project boundaries."""

    MAX_FILE_SIZE_MB = 1.0  # 1MB limit for reading files

    async def read_file(self, relative_path: str, user_id: Optional[str] = None) -> dict:
        """
        Read a file safely within project boundaries.

        Args:
            relative_path: Relative path to file
            user_id: User ID for context

        Returns:
            Dict with file content and metadata

        Raises:
            ValueError: If path is invalid or file is too large
            FileNotFoundError: If file doesn't exist
            PermissionError: If file cannot be read
        """
        # Resolve safe path
        file_path = resolve_safe_path(relative_path, user_id)

        # Check if file exists
        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {relative_path}")

        # Check if it's actually a file
        if not file_path.is_file():
            raise ValueError(f"Path is not a file: {relative_path}")

        # Check file size
        file_size_mb = get_file_size_mb(file_path)
        if file_size_mb > self.MAX_FILE_SIZE_MB:
            raise ValueError(f"File too large ({file_size_mb:.1f}MB > {self.MAX_FILE_SIZE_MB}MB): {relative_path}")

        # Check if it's a text file
        if not is_text_file(file_path):
            raise ValueError(f"File is not a text file: {relative_path}")

        # Read file content
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except UnicodeDecodeError:
            raise ValueError(f"File is not valid UTF-8 text: {relative_path}")
        except PermissionError:
            raise PermissionError(f"Permission denied reading file: {relative_path}")

        return {
            "content": content,
            "path": relative_path,
            "size": len(content),
            "encoding": "utf-8"
        }

    async def write_file(
        self,
        relative_path: str,
        content: str,
        user_id: Optional[str] = None
    ) -> dict:
        """
        Write content to a file safely within project boundaries.

        Args:
            relative_path: Relative path to file
            content: Content to write
            user_id: User ID for context

        Returns:
            Dict with success confirmation and metadata

        Raises:
            ValueError: If path is invalid
            PermissionError: If file cannot be written
        """
        # Resolve safe path
        file_path = resolve_safe_path(relative_path, user_id)

        # Ensure parent directory exists
        file_path.parent.mkdir(parents=True, exist_ok=True)

        # Write file content
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
        except PermissionError:
            raise PermissionError(f"Permission denied writing file: {relative_path}")

        return {
            "success": True,
            "path": relative_path,
            "size": len(content)
        }

    async def list_files(
        self,
        relative_path: str = ".",
        user_id: Optional[str] = None
    ) -> List[FileEntry]:
        """
        List files and directories in a path within project boundaries.

        Args:
            relative_path: Relative path to directory (defaults to project root)
            user_id: User ID for context

        Returns:
            List of file/directory entries

        Raises:
            ValueError: If path is invalid
            FileNotFoundError: If directory doesn't exist
        """
        # Resolve safe path
        dir_path = resolve_safe_path(relative_path, user_id)

        # Check if directory exists
        if not dir_path.exists():
            raise FileNotFoundError(f"Directory not found: {relative_path}")

        if not dir_path.is_dir():
            raise ValueError(f"Path is not a directory: {relative_path}")

        entries = []
        try:
            for item in sorted(dir_path.iterdir()):
                try:
                    stat = item.stat()
                    entry = FileEntry(
                        name=item.name,
                        path=str(item.relative_to(settings.project_root_path)),
                        is_dir=item.is_dir(),
                        size=stat.st_size if item.is_file() else None
                    )
                    entries.append(entry)
                except (OSError, PermissionError):
                    # Skip entries we can't access
                    continue
        except PermissionError:
            raise PermissionError(f"Permission denied listing directory: {relative_path}")

        return entries


# Global service instance
fs_service = FileSystemService()