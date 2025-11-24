const express = require('express');
const { spawn } = require('child_process');
const path = require('path');
const net = require('net');
const axios = require('axios');

const router = express.Router();

// Global variable to track MCP server process
let mcpProcess = null;
let mcpStatus = {
  running: false,
  serverId: 'mcp-server-1',
  uptime: '00:00:00',
  connections: 0,
  startTime: null,
  port: null,
  configJson: null
};

// Find an available port
function findAvailablePort(startPort = 5050) {
  return new Promise((resolve, reject) => {
    const server = net.createServer();
    server.listen(startPort, () => {
      const port = server.address().port;
      server.close(() => resolve(port));
    });
    server.on('error', () => {
      // Port is in use, try next one
      findAvailablePort(startPort + 1).then(resolve).catch(reject);
    });
  });
}

// Start MCP server
router.post('/start', async (req, res) => {
  try {
    // Check if user is authenticated
    if (!req.user || !req.user.userId) {
      return res.status(401).json({ error: 'Authentication required' });
    }

    // Check if MCP server is already running (either internally or externally)
    const axios = require('axios');
    const commonPorts = [5050, 5051, 5052, 8000, 8001];

    for (const port of commonPorts) {
      try {
        const response = await axios.get(`http://127.0.0.1:${port}/mcp/health`, {
          timeout: 1000
        });
        if (response.status === 200 && response.data?.server === 'SensCoder MCP') {
          // Server is already running externally
          mcpStatus.running = true;
          mcpStatus.port = port;
          mcpStatus.startTime = new Date(); // Approximate start time

          // Generate config JSON for Claude Desktop/Cursor
          const projectRoot = path.join(__dirname, '../../');
          const mcpPath = path.join(__dirname, '../../mcp-fastapi');
          mcpStatus.configJson = {
            mcpServers: {
              senscoder: {
                command: "uvicorn",
                args: ["app.main:app", "--host", "127.0.0.1", "--port", port.toString()],
                env: {
                  SENSCODER_PROJECT_ROOT: projectRoot,
                  SENSCODER_BACKEND_URL: "http://localhost:4000",
                  SENSCODER_ALLOW_EXEC: "false",
                  SENSCODER_ALLOW_GIT: "true",
                  SENSCODER_DEFAULT_USER_ID: req.user.userId,
                  MCP_JWT_SECRET: process.env.MCP_JWT_SECRET || 'development-secret-key'
                },
                cwd: mcpPath
              }
            }
          };

          // Automatically open wizard page in browser
          const wizardUrl = `http://127.0.0.1:${port}/wizard`;
          const { exec } = require('child_process');
          exec(`start ${wizardUrl}`, (error) => {
            if (error) {
              console.log(`Could not open browser automatically: ${error}`);
            } else {
              console.log(`Opened wizard page in browser: ${wizardUrl}`);
            }
          });

          return res.json({
            success: true,
            message: `MCP server is already running on port ${port}`,
            status: 'running',
            port: port,
            wizard_url: wizardUrl,
            configJson: mcpStatus.configJson
          });
        }
      } catch (error) {
        // Continue checking other ports
      }
    }

    // Check if we already have an internal process running
    if (mcpProcess && !mcpProcess.killed) {
      // Automatically open wizard page in browser
      const wizardUrl = `http://127.0.0.1:${mcpStatus.port}/wizard`;
      const { exec } = require('child_process');
      exec(`start ${wizardUrl}`, (error) => {
        if (error) {
          console.log(`Could not open browser automatically: ${error}`);
        } else {
          console.log(`Opened wizard page in browser: ${wizardUrl}`);
        }
      });

      return res.json({
        success: true,
        message: 'MCP server is already running',
        status: 'running',
        port: mcpStatus.port,
        wizard_url: wizardUrl,
        configJson: mcpStatus.configJson
      });
    }

    // Determine project root (use the workspace path)
    const projectRoot = path.join(__dirname, '../../');

    // Find available port
    const port = await findAvailablePort(5050);

    // Prepare environment variables
    const env = {
      ...process.env,
      SENSCODER_PROJECT_ROOT: projectRoot,
      SENSCODER_BACKEND_URL: 'http://localhost:4000',
      SENSCODER_ALLOW_EXEC: 'false',
      SENSCODER_ALLOW_GIT: 'true',
      SENSCODER_DEFAULT_USER_ID: req.user.userId,
      MCP_JWT_SECRET: process.env.MCP_JWT_SECRET || 'development-secret-key'
    };

    // Path to the MCP FastAPI server
    const mcpPath = path.join(__dirname, '../../mcp-fastapi');

    // Start the MCP server
    mcpProcess = spawn('python', ['-m', 'uvicorn', 'app.main:app', '--host', '127.0.0.1', '--port', port.toString()], {
      cwd: mcpPath,
      stdio: ['pipe', 'pipe', 'pipe'],
      detached: false,
      env: env
    });

    console.log(`Starting MCP server on port ${port} for user ${req.user.userId}`);

    // Capture stdout and stderr
    mcpProcess.stdout.on('data', (data) => {
      console.log(`MCP stdout: ${data}`);
    });

    mcpProcess.stderr.on('data', (data) => {
      console.error(`MCP stderr: ${data}`);
    });

    // Handle process events
    mcpProcess.on('error', (error) => {
      console.error('MCP server error:', error);
      mcpStatus.running = false;
      mcpStatus.startTime = null;
      mcpStatus.port = null;
      mcpStatus.configJson = null;
    });

    mcpProcess.on('exit', (code) => {
      console.log(`MCP server exited with code ${code}`);
      mcpStatus.running = false;
      mcpStatus.startTime = null;
      mcpStatus.port = null;
      mcpStatus.configJson = null;
    });

    // Wait for server to start
    await new Promise((resolve, reject) => {
      const timeout = setTimeout(() => {
        reject(new Error('MCP server startup timeout'));
      }, 30000); // 30 second timeout (increased from 10)

      const checkHealth = async () => {
        try {
          const response = await axios.get(`http://127.0.0.1:${port}/mcp/health`, {
            timeout: 2000
          });

          if (response.status === 200) {
            clearTimeout(timeout);
            resolve();
          }
        } catch (error) {
          // Server not ready yet, try again
          setTimeout(checkHealth, 500);
        }
      };

      // Start checking health after a brief delay
      setTimeout(checkHealth, 1000);
    });

    // Update status
    mcpStatus.running = true;
    mcpStatus.startTime = new Date();
    mcpStatus.connections = 1;
    mcpStatus.port = port;

    // Generate config JSON for Claude Desktop/Cursor
    mcpStatus.configJson = {
      mcpServers: {
        senscoder: {
          command: "uvicorn",
          args: ["app.main:app", "--host", "127.0.0.1", "--port", port.toString()],
          env: {
            SENSCODER_PROJECT_ROOT: projectRoot,
            SENSCODER_BACKEND_URL: "http://localhost:4000",
            SENSCODER_ALLOW_EXEC: "false",
            SENSCODER_ALLOW_GIT: "true",
            SENSCODER_DEFAULT_USER_ID: req.user.userId,
            MCP_JWT_SECRET: process.env.MCP_JWT_SECRET || 'development-secret-key'
          },
          cwd: mcpPath
        }
      }
    };

    // Automatically open wizard page in browser
    const wizardUrl = `http://127.0.0.1:${port}/wizard`;
    const { exec } = require('child_process');
    exec(`start ${wizardUrl}`, (error) => {
      if (error) {
        console.log(`Could not open browser automatically: ${error}`);
      } else {
        console.log(`Opened wizard page in browser: ${wizardUrl}`);
      }
    });

    res.json({
      success: true,
      message: `MCP server started successfully on port ${port}`,
      status: 'running',
      port: port,
      wizard_url: wizardUrl,
      configJson: mcpStatus.configJson
    });

  } catch (error) {
    console.error('Error starting MCP server:', error);

    // Clean up if process was started but health check failed
    if (mcpProcess && !mcpProcess.killed) {
      mcpProcess.kill('SIGTERM');
      setTimeout(() => {
        if (!mcpProcess.killed) {
          mcpProcess.kill('SIGKILL');
        }
      }, 5000);
    }

    mcpStatus.running = false;
    mcpStatus.startTime = null;
    mcpStatus.port = null;
    mcpStatus.configJson = null;

    res.status(500).json({
      error: 'Failed to start MCP server',
      details: error.message
    });
  }
});

// Stop MCP server
router.post('/stop', async (req, res) => {
  try {
    if (!mcpProcess || mcpProcess.killed) {
      return res.json({
        success: true,
        message: 'MCP server is not running'
      });
    }

    // Kill the process
    mcpProcess.kill('SIGTERM');

    // Wait for process to exit
    setTimeout(() => {
      if (!mcpProcess.killed) {
        mcpProcess.kill('SIGKILL');
      }
    }, 5000);

    // Update status
    mcpStatus.running = false;
    mcpStatus.startTime = null;
    mcpStatus.connections = 0;
    mcpStatus.port = null;
    mcpStatus.configJson = null;

    res.json({
      success: true,
      message: 'MCP server stopped successfully'
    });

  } catch (error) {
    console.error('Error stopping MCP server:', error);
    res.status(500).json({ error: 'Failed to stop MCP server' });
  }
});

// Get MCP server status
router.get('/status', async (req, res) => {
  try {
    // Calculate uptime
    let uptime = '00:00:00';
    if (mcpStatus.running && mcpStatus.startTime) {
      const now = new Date();
      const diff = now - mcpStatus.startTime;
      const hours = Math.floor(diff / (1000 * 60 * 60));
      const minutes = Math.floor((diff % (1000 * 60 * 60)) / (1000 * 60));
      const seconds = Math.floor((diff % (1000 * 60)) / 1000);
      uptime = `${hours.toString().padStart(2, '0')}:${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`;
    }

    const status = {
      running: mcpStatus.running,
      serverId: mcpStatus.serverId,
      uptime: uptime,
      connections: mcpStatus.connections,
      port: mcpStatus.port,
      projectRoot: path.join(__dirname, '../../mcp-fastapi'),
      configJson: mcpStatus.configJson
    };

    res.json(status);

  } catch (error) {
    console.error('Error getting MCP server status:', error);
    res.status(500).json({ error: 'Failed to get MCP server status' });
  }
});

module.exports = router;

// Export MCP status for use in other routes
module.exports.mcpStatus = mcpStatus;