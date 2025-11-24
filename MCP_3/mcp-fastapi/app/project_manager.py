"""Project configuration and wizard management."""
import json
import os
from pathlib import Path
from typing import Dict, Any, Optional
from pydantic import BaseModel, validator
from app.config import settings


class ProjectConfig(BaseModel):
    """Project configuration model."""
    project_root: str
    project_type: str  # 'nextjs', 'vite', 'node', 'python', 'other'
    port: Optional[int] = None
    test_command: Optional[str] = None
    build_command: Optional[str] = None
    start_command: Optional[str] = None
    custom_settings: Optional[Dict[str, Any]] = None

    @validator('project_root')
    def validate_project_root(cls, v):
        """Validate that project root exists and is a directory."""
        path = Path(v).resolve()
        if not path.exists():
            raise ValueError(f"Project root does not exist: {path}")
        if not path.is_dir():
            raise ValueError(f"Project root is not a directory: {path}")
        return str(path)

    @property
    def project_path(self) -> Path:
        """Get the project root as a Path object."""
        return Path(self.project_root)


class ProjectManager:
    """Manages project configuration and Vercel integration."""

    def __init__(self):
        self.config_file = Path.home() / ".senscoder" / "project_config.json"
        self.config_file.parent.mkdir(parents=True, exist_ok=True)
        self._config: Optional[ProjectConfig] = None
        self._load_config()

    def _load_config(self):
        """Load project configuration from disk."""
        if self.config_file.exists():
            try:
                with open(self.config_file, 'r') as f:
                    data = json.load(f)
                    self._config = ProjectConfig(**data)
            except Exception:
                self._config = None

    def _save_config(self):
        """Save project configuration to disk."""
        if self._config:
            with open(self.config_file, 'w') as f:
                json.dump(self._config.dict(), f, indent=2)

    def set_project_config(self, config: ProjectConfig):
        """Set the project configuration."""
        self._config = config
        self._save_config()

    def get_project_config(self) -> Optional[ProjectConfig]:
        """Get the current project configuration."""
        return self._config

    def get_project_root(self) -> Optional[str]:
        """Get the current project root path."""
        return self._config.project_root if self._config else None

    def is_configured(self) -> bool:
        """Check if project is configured."""
        return self._config is not None

    async def get_vercel_config(self) -> Dict[str, Any]:
        """Fetch configuration from Vercel backend."""
        try:
            import httpx
            async with httpx.AsyncClient() as client:
                response = await client.get(f"{settings.senscoder_backend_url}/api/internal/mcp/config")
                if response.status_code == 200:
                    return response.json()
                else:
                    return {}
        except Exception:
            return {}


# Global project manager instance
project_manager = ProjectManager()