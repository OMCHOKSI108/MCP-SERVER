"""Configuration management for SensCoder MCP Server."""
import os
from pathlib import Path
from typing import Optional, List

from pydantic import validator
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # Required settings
    senscoder_project_root: str

    # Optional settings with defaults
    senscoder_backend_url: str = "http://localhost:4000"
    senscoder_allow_exec: bool = False
    senscoder_allow_git: bool = True
    senscoder_default_user_id: Optional[str] = None

    # Server settings
    host: str = "127.0.0.1"
    port: int = 5050
    debug: bool = False

    # CORS settings
    cors_origins_str: str = "http://localhost:3000,http://127.0.0.1:3000"

    @property
    def cors_origins(self) -> List[str]:
        """Parse CORS origins from comma-separated string."""
        return [origin.strip() for origin in self.cors_origins_str.split(",") if origin.strip()]

    # Rate limiting settings
    rate_limit_requests: int = 100
    rate_limit_window: int = 60  # seconds
    tool_invoke_rate_limit: str = "10/minute"

    # Security settings
    mcp_jwt_secret: str = "your-secret-key-change-in-production"

    class Config:
        env_file = ".env"
        case_sensitive = False

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._validate_critical_settings()

    def _validate_critical_settings(self):
        """Validate critical security settings."""
        if self.mcp_jwt_secret == "your-secret-key-change-in-production":
            if not self.debug:
                raise ValueError("MCP_JWT_SECRET must be set to a secure value in production")

        if self.senscoder_allow_exec and not self.debug:
            print("WARNING: Command execution is enabled in production. Ensure this is intentional.")

    @validator("senscoder_project_root")
    def validate_project_root(cls, v):
        """Validate that project root exists and is a directory."""
        path = Path(v).resolve()
        if not path.exists():
            raise ValueError(f"Project root does not exist: {path}")
        if not path.is_dir():
            raise ValueError(f"Project root is not a directory: {path}")
        return str(path)

    @property
    def project_root_path(self) -> Path:
        """Get the project root as a Path object."""
        return Path(self.senscoder_project_root)

    def get_backend_url(self, endpoint: str) -> str:
        """Construct a full backend URL for the given endpoint."""
        return f"{self.senscoder_backend_url.rstrip('/')}/{endpoint.lstrip('/')}"


# Global settings instance
settings = Settings()