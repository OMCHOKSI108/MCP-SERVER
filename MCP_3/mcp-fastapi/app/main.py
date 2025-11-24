"""FastAPI application entry point for SensCoder MCP Server."""
import logging
import uvicorn
from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware

from app.config import settings
from app.routes import router
from app.wizard_routes import router as wizard_router


# Configure logging
logging.basicConfig(
    level=logging.INFO if not settings.debug else logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Configure rate limiting
limiter = Limiter(
    key_func=get_remote_address,
    default_limits=[f"{settings.rate_limit_requests}/minute"]
)


def create_app() -> FastAPI:
    """Create and configure the FastAPI application."""
    app = FastAPI(
        title="SensCoder MCP Server",
        description="Model Context Protocol server for SensCoder local-first coding assistant",
        version="0.1.0",
        docs_url="/docs",
        redoc_url="/redoc"
    )

    # Add rate limiting
    app.state.limiter = limiter
    app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
    app.add_middleware(SlowAPIMiddleware)

    # Add CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Add error handling middleware
    @app.exception_handler(HTTPException)
    async def http_exception_handler(request, exc):
        logger.error(f"HTTP error: {exc.status_code} - {exc.detail}")
        return JSONResponse(
            status_code=exc.status_code,
            content={"error": exc.detail},
        )

    @app.exception_handler(Exception)
    async def general_exception_handler(request, exc):
        logger.error(f"Unexpected error: {str(exc)}", exc_info=True)
        return JSONResponse(
            status_code=500,
            content={"error": "Internal server error"},
        )

    # Add request logging middleware
    @app.middleware("http")
    async def log_requests(request: Request, call_next):
        logger.info(f"Request: {request.method} {request.url}")
        response = await call_next(request)
        logger.info(f"Response: {response.status_code}")
        return response

    # Include MCP routes
    app.include_router(router)
    app.include_router(wizard_router)

    # Root endpoint
    @app.get("/")
    async def root():
        """Root endpoint with server information."""
        from app.project_manager import project_manager
        config = project_manager.get_project_config()

        return {
            "name": "SensCoder MCP Server",
            "version": "0.1.0",
            "description": "Local-first coding assistant MCP server",
            "configured": project_manager.is_configured(),
            "project_root": config.project_root if config else None,
            "project_type": config.project_type if config else None,
            "endpoints": {
                "docs": "/docs",
                "health": "/mcp/health",
                "tools": "/mcp/tool-invoke",
                "resources": "/mcp/resources",
                "prompts": "/mcp/prompts",
                "wizard": "/wizard",
                "wizard_status": "/wizard/status"
            }
        }

    return app


# Create the FastAPI app instance
app = create_app()


def main():
    """Main entry point for running the server."""
    uvicorn.run(
        "app.main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug,
        log_level="info"
    )


if __name__ == "__main__":
    main()