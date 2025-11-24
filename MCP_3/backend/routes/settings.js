const express = require('express');
const User = require('../models/User');
const bcrypt = require('bcryptjs');

const router = express.Router();

// GET /api/settings - Get user settings
router.get('/', async (req, res) => {
  try {
    const user = await User.findById(req.user.userId).select('+apiKey');
    if (!user) {
      return res.status(404).json({ message: 'User not found' });
    }

    const settings = {
      provider: user.apiProvider || 'gemini',
      hasApiKey: user.hasApiKey || false,
      theme: user.theme || 'dark',
      language: user.language || 'en',
      notifications: user.notifications !== false
    };

    res.json(settings);

  } catch (error) {
    console.error('Get settings error:', error);
    res.status(500).json({ message: 'Internal server error' });
  }
});

// PUT /api/settings - Update user settings
router.put('/', async (req, res) => {
  try {
    const user = await User.findById(req.user.userId);
    if (!user) {
      return res.status(404).json({ message: 'User not found' });
    }

    const { provider, hasApiKey, apiKey, theme, language, notifications, name } = req.body;

    // Update user fields
    if (name) user.name = name;
    if (provider) user.apiProvider = provider;
    if (theme) user.theme = theme;
    if (language) user.language = language;
    if (notifications !== undefined) user.notifications = notifications;

    // Handle API key
    if (hasApiKey && apiKey) {
      // Encrypt API key before storing
      const saltRounds = 12;
      user.apiKey = await bcrypt.hash(apiKey, saltRounds);
      user.hasApiKey = true;
    } else if (!hasApiKey) {
      user.apiKey = undefined;
      user.hasApiKey = false;
    }

    await user.save();

    res.json({
      message: 'Settings updated successfully',
      settings: {
        provider: user.apiProvider,
        hasApiKey: user.hasApiKey,
        theme: user.theme,
        language: user.language,
        notifications: user.notifications
      }
    });

  } catch (error) {
    console.error('Update settings error:', error);
    res.status(500).json({ message: 'Internal server error' });
  }
});

// Helper function to decrypt API key for use (in a real app, you'd use proper encryption)
const getDecryptedApiKey = async (encryptedKey, providedKey) => {
  // For demo purposes, we'll just return the provided key
  // In production, you'd decrypt the stored encrypted key
  return providedKey;
};

module.exports = router;