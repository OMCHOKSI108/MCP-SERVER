const express = require('express');
const router = express.Router();

// Get integration status
router.get('/status', async (req, res) => {
  try {
    // Import MCP status from mcp route
    const mcpRoute = require('./mcp');

    // Check if MCP server is actually running by testing health endpoint
    let mcpRunning = false;
    let mcpPort = null;
    let mcpStartTime = null;

    // First check internal status
    if (mcpRoute.mcpStatus?.running && mcpRoute.mcpStatus?.port) {
      try {
        // Test the health endpoint
        const axios = require('axios');
        const response = await axios.get(`http://127.0.0.1:${mcpRoute.mcpStatus.port}/mcp/health`, {
          timeout: 2000
        });
        if (response.status === 200) {
          mcpRunning = true;
          mcpPort = mcpRoute.mcpStatus.port;
          mcpStartTime = mcpRoute.mcpStatus.startTime;
        }
      } catch (error) {
        // Health check failed, server might not be running
        console.log('MCP health check failed, marking as not running');
      }
    }

    // If internal status shows not running, check common ports for external MCP server
    if (!mcpRunning) {
      const axios = require('axios');
      const commonPorts = [5050, 5051, 5052, 8000, 8001];

      for (const port of commonPorts) {
        try {
          const response = await axios.get(`http://127.0.0.1:${port}/mcp/health`, {
            timeout: 1000
          });
          if (response.status === 200 && response.data?.server === 'SensCoder MCP') {
            mcpRunning = true;
            mcpPort = port;
            mcpStartTime = new Date(); // We don't know when it started externally
            break;
          }
        } catch (error) {
          // Continue checking other ports
        }
      }
    }

    const status = {
      providers: {
        gemini: {
          hasKey: true,
          isConfigured: true
        },
        openai: {
          hasKey: false,
          isConfigured: false
        }
      },
      mcp: {
        status: mcpRunning ? 'running' : 'stopped',
        port: mcpPort,
        lastStarted: mcpStartTime
      },
      settings: {
        provider: 'gemini',
        useOwnKey: false,
        hasApiKey: true,
        theme: 'dark',
        projectRoot: process.cwd()
      }
    };

    res.json(status);
  } catch (error) {
    console.error('Error getting integration status:', error);
    res.status(500).json({ error: 'Failed to get integration status' });
  }
});

module.exports = router;