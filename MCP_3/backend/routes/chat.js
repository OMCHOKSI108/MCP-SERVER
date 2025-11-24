const express = require('express');
const User = require('../models/User');
const { GoogleGenerativeAI } = require('@google/generative-ai');
const ActivityLog = require('../models/ActivityLog');

const router = express.Router();

// POST /api/chat - Send message to AI
router.post('/', async (req, res) => {
  try {
    const { messages } = req.body;
    const userId = req.user?.userId;

    if (!userId) {
      return res.status(401).json({ message: 'Authentication required' });
    }

    if (!messages || !Array.isArray(messages)) {
      return res.status(400).json({ message: 'Messages array is required' });
    }

    // Get user settings
    const user = await User.findById(userId).select('+apiKey');
    if (!user) {
      return res.status(404).json({ message: 'User not found' });
    }

    // Check if user is banned or blocked
    if (user.isBanned || user.isBlocked) {
      return res.status(403).json({ message: 'Account access restricted' });
    }

    // Check daily message limit
    const dailyLimit = user.hasApiKey ? 1000 : 20; // Higher limit for users with own API keys
    if (user.dailyMessages >= dailyLimit) {
      return res.status(429).json({ message: `Daily message limit (${dailyLimit}) exceeded. Please try again tomorrow.` });
    }

    let apiKey;
    let useSharedKey = false;

    // Check if user has their own API key
    if (user.hasApiKey && user.apiKey) {
      // For demo purposes, we'll use a shared key since we can't decrypt
      // In production, you'd decrypt the stored API key
      apiKey = process.env.GEMINI_API_KEY; // Use shared key for now
    } else {
      // Use shared API key
      apiKey = process.env.GEMINI_API_KEY;
      useSharedKey = true;
    }

    if (!apiKey) {
      console.log('GEMINI_API_KEY not configured in environment variables');
      return res.status(500).json({ message: 'AI service not configured. Please set GEMINI_API_KEY in environment variables.' });
    }

    // Initialize Gemini AI
    const genAI = new GoogleGenerativeAI(apiKey);
    const model = genAI.getGenerativeModel({ model: 'gemini-2.5-flash' });

    // System prompt for MCP server development
    const systemPrompt = `You are an expert AI assistant specialized in building Model Context Protocol (MCP) servers. Your role is to help developers create, configure, and deploy MCP servers that integrate AI capabilities with various tools and services.

Key responsibilities:
- Guide users through MCP server development using best practices
- Provide code examples for MCP server implementation
- Help with tool integration and configuration
- Assist with debugging and troubleshooting MCP servers
- Explain MCP concepts and architecture clearly
- Suggest optimal patterns for different use cases

When responding:
- Always provide well-formatted, actionable code examples
- Include proper error handling and validation
- Explain complex concepts with clear analogies
- Suggest testing strategies and deployment considerations
- Be concise but comprehensive in your explanations
- **Format your responses using clean Markdown:**
  - Use **bold** for emphasis and key terms
  - Use ### headings for sections
  - Use - bullet points for lists
  - Use numbered lists for steps
  - Use proper code blocks with language hints: \`\`\`javascript, \`\`\`python, etc.
  - Use > blockquotes for important notes
  - Use tables when comparing options

Remember: MCP servers should be secure, efficient, and well-documented. Always prioritize code quality and best practices.`;

    // Convert messages to Gemini format with system prompt
    const lastMessage = messages[messages.length - 1];
    const userPrompt = lastMessage.content;

    // Combine system prompt with user message
    const fullPrompt = `${systemPrompt}\n\nUser Query: ${userPrompt}`;

    // Generate response
    const result = await model.generateContent(fullPrompt);
    const response = await result.response;
    let aiResponse = response.text();

    // Clean up and format the response
    aiResponse = aiResponse.trim();

    // If response contains code blocks, ensure proper formatting
    if (aiResponse.includes('```')) {
      aiResponse = aiResponse.replace(/```\s*(\w+)/g, '```$1');
    }

    // Update user usage
    await User.findByIdAndUpdate(userId, {
      $inc: { dailyMessages: 1 },
      lastActivity: new Date()
    });

    // Log the message activity
    await ActivityLog.logActivity({
      userId: userId,
      action: 'message_sent',
      message: 'User sent a message to AI chat',
      details: {
        messageCount: user.dailyMessages + 1,
        dailyLimit: useSharedKey ? 20 : 1000,
        usedSharedKey: useSharedKey
      },
      ipAddress: req.ip,
      userAgent: req.get('User-Agent'),
      level: 'info'
    });

    // Update usage (in a real app, you'd track this properly)
    const usage = {
      messageCount: user.dailyMessages + 1,
      dailyLimit: useSharedKey ? 20 : 1000 // Higher limit for own keys
    };

    res.json({
      response: aiResponse,
      usage: usage
    });

  } catch (error) {
    console.error('Chat error:', error);
    res.status(500).json({ message: 'Sorry, I encountered an error. Please try again.' });
  }
});

module.exports = router;