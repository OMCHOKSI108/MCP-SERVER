# SensCoder MCP Server - Complete Setup and Usage Guidelines

## Table of Contents
1. [Quick Start](#quick-start)
2. [System Requirements](#system-requirements)
3. [Installation Guide](#installation-guide)
4. [Configuration](#configuration)
5. [Running the Server](#running-the-server)
6. [API Testing](#api-testing)
7. [Claude Desktop Integration](#claude-desktop-integration)
8. [Available Tools](#available-tools)
9. [Security Guidelines](#security-guidelines)
10. [Troubleshooting](#troubleshooting)
11. [Development Guidelines](#development-guidelines)

## Quick Start

### Prerequisites
- Python 3.8+
- Node.js 16+ (for frontend/backend)
- Git

### One-Command Setup
```bash
# Clone and setup MCP server
cd mcp-fastapi
pip install -e .
export SENSCODER_PROJECT_ROOT="$(pwd)/.."
python -m app.main
```

## System Requirements

### Minimum Requirements
- **OS**: Windows 10+, macOS 10.15+, Ubuntu 18.04+
- **Python**: 3.8 or higher
- **RAM**: 2GB minimum, 4GB recommended
- **Storage**: 500MB free space
- **Network**: Internet connection for backend integration

### Recommended Requirements
- **Python**: 3.10+
- **RAM**: 8GB+
- **Storage**: 2GB+ free space
- **CPU**: Multi-core processor

## Installation Guide

### Step 1: Clone Repository
```bash
git clone <repository-url>
cd MCP_3
```

### Step 2: Setup MCP Server
```bash
cd mcp-fastapi

# Create virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -e .
```

### Step 3: Environment Configuration
```bash
# Copy environment template
cp .env.example .env

# Edit .env file with your settings
nano .env  # or use your preferred editor
```

### Step 4: Verify Installation
```bash
# Test import
python -c "from app.main import app; print('MCP Server installed successfully')"

# Check health endpoint (after starting server)
curl http://localhost:5050/mcp/health
```

## Configuration

### Environment Variables

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `SENSCODER_PROJECT_ROOT` | Absolute path to project root | - | Yes |
| `SENSCODER_BACKEND_URL` | SensCoder backend URL | `http://localhost:4000` | No |
| `SENSCODER_ALLOW_EXEC` | Enable command execution | `false` | No |
| `SENSCODER_ALLOW_GIT` | Enable git operations | `true` | No |
| `SENSCODER_DEFAULT_USER_ID` | Default user ID for testing | - | No |
| `MCP_JWT_SECRET` | JWT secret for authentication | - | Yes (production) |
| `DEBUG` | Enable debug mode | `false` | No |

### Sample .env Configuration
```env
# Project Configuration
SENSCODER_PROJECT_ROOT=/absolute/path/to/your/project
SENSCODER_BACKEND_URL=http://localhost:4000

# Feature Flags
SENSCODER_ALLOW_EXEC=false
SENSCODER_ALLOW_GIT=true
SENSCODER_DEFAULT_USER_ID=test-user-123

# Security
MCP_JWT_SECRET=your-secure-jwt-secret-here

# Development
DEBUG=true
CORS_ORIGINS_STR=http://localhost:3000,http://127.0.0.1:3000
```

## Running the Server

### Development Mode
```bash
# From mcp-fastapi directory
python -m app.main
```
- Server starts on `http://127.0.0.1:5050`
- Auto-reload enabled for development
- Debug logging enabled

### Production Mode
```bash
# Using uvicorn directly
uvicorn app.main:app --host 0.0.0.0 --port 5050

# Or using gunicorn (recommended for production)
gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:5050
```

### Docker Deployment
```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 5050

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "5050"]
```

## API Testing

### Health Check
```bash
curl http://localhost:5050/mcp/health
```

Response:
```json
{
  "status": "healthy",
  "server": "SensCoder MCP",
  "version": "0.1.0",
  "tools_count": 8,
  "resources_count": 1,
  "prompts_count": 3
}
```

### Authentication
```bash
# Get JWT token
curl -X POST http://localhost:5050/mcp/auth/login \
  -H "Content-Type: application/json" \
  -d '{"user_id": "test-user-123"}'
```

### Tool Invocation
```bash
# Echo tool
curl -X POST http://localhost:5050/mcp/tool-invoke \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -d '{
    "tool": "echo",
    "params": {"text": "Hello MCP Server!"},
    "user_id": "test-user-123"
  }'
```

### Get Resources
```bash
curl http://localhost:5050/mcp/resources
```

### Get Prompts
```bash
curl http://localhost:5050/mcp/prompts
```

## Claude Desktop Integration

### Configuration File Location
- **Windows**: `%APPDATA%\Claude\claude_desktop_config.json`
- **macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
- **Linux**: `~/.config/Claude/claude_desktop_config.json`

### Configuration Template
```json
{
  "mcpServers": {
    "senscoder-fastapi": {
      "command": "uvicorn",
      "args": ["app.main:app", "--host", "127.0.0.1", "--port", "5050"],
      "env": {
        "SENSCODER_PROJECT_ROOT": "/absolute/path/to/project",
        "SENSCODER_BACKEND_URL": "http://localhost:4000",
        "SENSCODER_ALLOW_EXEC": "false",
        "SENSCODER_ALLOW_GIT": "true",
        "MCP_JWT_SECRET": "your-secure-jwt-secret"
      }
    }
  }
}
```

### Testing Integration
1. Save the configuration file
2. Restart Claude Desktop
3. Check if MCP server appears in Claude's tools
4. Try asking Claude: "What files are in the current directory?"

## Available Tools

### Core Tools
- **echo**: Test connectivity by echoing text
- **math**: Safe mathematical expression evaluation

### File System Tools
- **read_file**: Read text files within project boundaries
- **write_file**: Create or modify text files
- **list_files**: List directory contents

### System Tools
- **exec**: Execute shell commands (when enabled)
- **git**: Git operations (status, log, diff, etc.)

### Configuration Tools
- **get_provider_config**: Get AI provider settings from backend

### Tool Usage Examples

#### File Operations
```bash
# Read a file
curl -X POST http://localhost:5050/mcp/tool-invoke \
  -H "Authorization: Bearer TOKEN" \
  -d '{
    "tool": "read_file",
    "params": {"path": "README.md"},
    "user_id": "test-user"
  }'

# List directory
curl -X POST http://localhost:5050/mcp/tool-invoke \
  -H "Authorization: Bearer TOKEN" \
  -d '{
    "tool": "list_files",
    "params": {"path": "."},
    "user_id": "test-user"
  }'
```

#### Git Operations
```bash
# Git status
curl -X POST http://localhost:5050/mcp/tool-invoke \
  -H "Authorization: Bearer TOKEN" \
  -d '{
    "tool": "git",
    "params": {"subcommand": "status", "args": []},
    "user_id": "test-user"
  }'
```

#### Math Evaluation
```bash
# Calculate expression
curl -X POST http://localhost:5050/mcp/tool-invoke \
  -H "Authorization: Bearer TOKEN" \
  -d '{
    "tool": "math",
    "params": {"expression": "2 + 3 * 4"},
    "user_id": "test-user"
  }'
```

## Security Guidelines

### Path Sandboxing
- All file operations are restricted to `SENSCODER_PROJECT_ROOT`
- Path traversal attacks are prevented
- Symlink following is controlled

### Command Execution
- Disabled by default (`SENSCODER_ALLOW_EXEC=false`)
- When enabled, dangerous commands are filtered
- Command execution is logged and monitored

### Authentication
- JWT-based authentication for tool invocation
- Token expiration and refresh mechanisms
- User-specific access controls

### Rate Limiting
- Configurable request limits per minute
- Tool-specific rate limits
- Automatic throttling for abuse prevention

### Best Practices
1. **Use strong JWT secrets** in production
2. **Enable command execution only when necessary**
3. **Regularly update dependencies**
4. **Monitor server logs for suspicious activity**
5. **Use HTTPS in production**
6. **Implement proper firewall rules**

## Troubleshooting

### Common Issues

#### Server Won't Start
```bash
# Check Python version
python --version

# Check if port is available
netstat -an | findstr :5050

# Check environment variables
echo $SENSCODER_PROJECT_ROOT

# Run with verbose logging
DEBUG=true python -m app.main
```

#### Authentication Errors
```bash
# Verify JWT token
curl -X POST http://localhost:5050/mcp/auth/login \
  -d '{"user_id": "test-user"}'

# Check token in subsequent requests
curl -H "Authorization: Bearer YOUR_TOKEN" \
  http://localhost:5050/mcp/health
```

#### Tool Invocation Errors
```bash
# Check tool availability
curl http://localhost:5050/mcp/health

# Verify tool parameters
curl -X POST http://localhost:5050/mcp/tool-invoke \
  -H "Authorization: Bearer TOKEN" \
  -d '{
    "tool": "echo",
    "params": {"text": "test"},
    "user_id": "test-user"
  }'
```

#### Claude Desktop Integration Issues
```bash
# Check Claude configuration file
cat ~/Library/Application\ Support/Claude/claude_desktop_config.json

# Verify server is running
curl http://localhost:5050/mcp/health

# Check Claude Desktop logs
# (Location varies by OS)
```

### Debug Mode
Enable debug mode for detailed logging:
```bash
export DEBUG=true
python -m app.main
```

### Log Analysis
```bash
# View recent logs
tail -f /path/to/logs/mcp_server.log

# Search for errors
grep "ERROR" /path/to/logs/mcp_server.log
```

## Development Guidelines

### Code Structure
```
app/
├── main.py              # FastAPI application entry
├── config.py            # Environment configuration
├── models.py            # Pydantic data models
├── routes.py            # HTTP endpoint definitions
├── mcp_server.py       # Core MCP logic and tools
├── auth.py              # Authentication services
├── services/            # Business logic services
│   ├── fs_service.py    # File system operations
│   ├── exec_service.py  # Command execution
│   ├── git_service.py   # Git operations
│   └── config_service.py # Configuration management
└── utils/               # Utility functions
    ├── path_utils.py    # Path validation utilities
    ├── subprocess_utils.py # Safe subprocess handling
    └── http_client.py   # HTTP client utilities
```

### Adding New Tools
1. **Define tool function** in `mcp_server.py`:
```python
async def _tool_your_tool(self, params: Dict[str, Any], user_id: Optional[str]) -> Dict[str, Any]:
    """Your tool description."""
    # Implementation here
    return result
```

2. **Register tool** in `_register_tools()`:
```python
self.tools['your_tool'] = self._tool_your_tool
```

3. **Add input validation** and error handling
4. **Update documentation**

### Testing Guidelines
```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_tools.py

# Run with coverage
pytest --cov=app --cov-report=html

# Run integration tests
pytest tests/integration/
```

### Code Quality
```bash
# Format code
black app/
isort app/

# Type checking
mypy app/

# Lint code
flake8 app/
```

### Performance Optimization
- Use async/await for I/O operations
- Implement proper caching for frequently accessed data
- Monitor memory usage and implement limits
- Use connection pooling for external services

### Deployment Checklist
- [ ] Environment variables configured
- [ ] JWT secret set securely
- [ ] HTTPS enabled
- [ ] Rate limiting configured
- [ ] Monitoring and logging set up
- [ ] Backup strategy implemented
- [ ] Security headers configured
- [ ] Load balancer configured (if needed)

---

## Support

For issues and questions:
1. Check the troubleshooting section above
2. Review server logs for error details
3. Test with minimal configuration
4. Create an issue with full error logs and configuration

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Ensure all tests pass
6. Submit a pull request

## License

This project is licensed under the MIT License. See LICENSE file for details.