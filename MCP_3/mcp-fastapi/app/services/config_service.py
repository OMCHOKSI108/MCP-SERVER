"""Configuration service for fetching user and project config from Vercel backend."""
import httpx
from typing import Dict, Any, Optional

from app.config import settings
from app.models import ProviderConfig
from app.project_manager import project_manager


class ConfigService:
    """Service for fetching configuration from the SensCoder Vercel backend."""

    async def get_provider_config(self, user_id: str) -> ProviderConfig:
        """
        Get provider configuration for a user from the Vercel backend.

        Args:
            user_id: User ID to get config for

        Returns:
            ProviderConfig object
        """
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.get(
                    f"{settings.senscoder_backend_url}/api/internal/mcp/config",
                    headers={"X-User-ID": user_id}
                )

                if response.status_code == 200:
                    config_data = response.json()
                    return ProviderConfig(
                        provider=config_data.get('provider', 'none'),
                        use_own_key=config_data.get('useOwnKey', False),
                        has_api_key=config_data.get('hasApiKey', False)
                    )
                else:
                    # Fallback to defaults
                    return self.get_default_provider_config()

        except Exception as e:
            print(f"Failed to fetch provider config: {e}")
            return self.get_default_provider_config()

    async def get_project_config(self, user_id: str) -> Dict[str, Any]:
        """
        Get project configuration for a user from the Vercel backend.

        Args:
            user_id: User ID to get project config for

        Returns:
            Project configuration dict
        """
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.get(
                    f"{settings.senscoder_backend_url}/api/internal/mcp/project-config",
                    headers={"X-User-ID": user_id}
                )

                if response.status_code == 200:
                    return response.json()
                else:
                    return self.get_default_project_config()

        except Exception as e:
            print(f"Failed to fetch project config: {e}")
            return self.get_default_project_config()

    def get_default_provider_config(self) -> ProviderConfig:
        """Get default provider config when backend is unavailable."""
        return ProviderConfig(
            provider='none',
            use_own_key=False,
            has_api_key=False
        )

    def get_default_project_config(self) -> Dict[str, Any]:
        """Get default project config when backend is unavailable."""
        config = project_manager.get_project_config()
        return {
            'projectRoot': config.project_root if config else str(settings.project_root_path)
        }


# Global service instance
config_service = ConfigService()