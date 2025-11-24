"""HTTP client for communicating with the SensCoder Node.js backend."""
import logging
import httpx
from typing import Dict, Any, Optional

from app.config import settings

logger = logging.getLogger(__name__)


class BackendClient:
    """Client for communicating with the SensCoder backend."""

    def __init__(self):
        self.client = httpx.AsyncClient(
            timeout=httpx.Timeout(10.0, connect=5.0),
            headers={
                "User-Agent": "SensCoder-MCP/0.1.0",
                "Content-Type": "application/json"
            },
            verify=True  # Enable SSL verification
        )

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.client.aclose()

    async def get_provider_config(self, user_id: str) -> Dict[str, Any]:
        """
        Get provider configuration for a user.

        Args:
            user_id: User ID to get config for

        Returns:
            Provider configuration dict
        """
        url = settings.get_backend_url(f"/internal/mcp/config?userId={user_id}")

        try:
            logger.info(f"Fetching provider config for user {user_id}")
            response = await self.client.get(url)
            response.raise_for_status()
            data = response.json()
            logger.info(f"Successfully retrieved provider config for user {user_id}")
            return data
        except httpx.HTTPError as e:
            logger.warning(f"Failed to get provider config for user {user_id}: {e}")
            # Return default config if backend is unavailable
            return {
                "provider": "none",
                "useOwnKey": False,
                "hasApiKey": False
            }
        except Exception as e:
            logger.error(f"Unexpected error getting provider config for user {user_id}: {e}")
            return {
                "provider": "none",
                "useOwnKey": False,
                "hasApiKey": False
            }

    async def get_project_config(self, user_id: str) -> Dict[str, Any]:
        """
        Get project configuration for a user.

        Args:
            user_id: User ID to get project config for

        Returns:
            Project configuration dict
        """
        url = settings.get_backend_url(f"/internal/mcp/project?userId={user_id}")

        try:
            logger.info(f"Fetching project config for user {user_id}")
            response = await self.client.get(url)
            response.raise_for_status()
            data = response.json()
            logger.info(f"Successfully retrieved project config for user {user_id}")
            return data
        except httpx.HTTPError as e:
            logger.warning(f"Failed to get project config for user {user_id}: {e}")
            # Return default project config
            return {
                "projectRoot": str(settings.project_root_path)
            }
        except Exception as e:
            logger.error(f"Unexpected error getting project config for user {user_id}: {e}")
            return {
                "projectRoot": str(settings.project_root_path)
            }


# Global client instance
backend_client = BackendClient()