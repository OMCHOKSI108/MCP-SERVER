# SensCoder MCP Server

A FastAPI-based Model Context Protocol (MCP) server for the SensCoder local-first coding assistant.

## Features

- **File Operations**: Safe read/write/list operations within project boundaries
- **Command Execution**: Controlled shell command execution with safety checks
- **Git Integration**: Git status, log, diff, and other operations
- **Provider Configuration**: Integration with SensCoder backend for AI provider settings
- **MCP Resources**: Server information and capabilities
- **MCP Prompts**: Code review, testing, and debugging templates

## Installation

1. **Clone and navigate to the project:**
   ```bash
   cd mcp-fastapi
   ```

2. **Install dependencies:**
   ```bash
   pip install -e .
   ```

3. **Set environment variables:**
   ```bash
   export SENSCODER_PROJECT_ROOT="/path/to/your/project"
   export SENSCODER_BACKEND_URL="http://localhost:4000"
   export SENSCODER_ALLOW_EXEC="false"
   export SENSCODER_ALLOW_GIT="true"
   ```

## Configuration

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `SENSCODER_PROJECT_ROOT` | Absolute path to project root | - | Yes |
| `SENSCODER_BACKEND_URL` | SensCoder backend URL | `http://localhost:4000` | No |
| `SENSCODER_ALLOW_EXEC` | Enable command execution | `false` | No |
| `SENSCODER_ALLOW_GIT` | Enable git operations | `true` | No |
| `SENSCODER_DEFAULT_USER_ID` | Default user ID for testing | - | No |

## Running the Server

### Development
```bash
python -m app.main
```

### Production
```bash
uvicorn app.main:app --host 0.0.0.0 --port 5050
```

## API Endpoints

- `POST /mcp/tool-invoke` - Invoke MCP tools
- `GET /mcp/resources` - Get available resources
- `GET /mcp/prompts` - Get available prompts
- `GET /mcp/health` - Health check

## Available Tools

### Core Tools
- `echo` - Echo text back (for connectivity testing)
- `math` - Safe mathematical expression evaluation

### File System Tools
- `read_file` - Read text files within project boundaries
- `write_file` - Write/create text files
- `list_files` - List directory contents

### System Tools
- `exec` - Execute shell commands (when enabled)
- `git` - Git operations (status, log, diff, etc.)

### Configuration Tools
- `get_provider_config` - Get AI provider settings from backend

## Claude Desktop Integration

Add this configuration to your `claude_desktop_config.json`:

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
        "SENSCODER_ALLOW_GIT": "true"
      }
    }
  }
}
```

## Safety Features

- **Path Sandboxing**: All file operations are restricted to the project root
- **Command Filtering**: Dangerous commands are blocked
- **Size Limits**: File reading is limited to 1MB
- **Timeout Protection**: Long-running operations are terminated
- **Permission Checks**: Operations respect file system permissions

## Development

### Running Tests
```bash
pytest
```

### Code Formatting
```bash
black app/
isort app/
```

### Type Checking
```bash
mypy app/
```

## Architecture

```
app/
├── main.py              # FastAPI application
├── config.py            # Environment configuration
├── models.py            # Pydantic models
├── routes.py            # HTTP endpoints
├── mcp_server.py       # Core MCP logic
├── services/            # Business logic services
│   ├── fs_service.py
│   ├── exec_service.py
│   ├── git_service.py
│   └── config_service.py
└── utils/               # Utility functions
    ├── path_utils.py
    ├── subprocess_utils.py
    └── http_client.py
```

## License

MIT License