const express = require('express');
const User = require('../models/User');
const GeminiKey = require('../models/GeminiKey');
const SystemSetting = require('../models/SystemSetting');
const ActivityLog = require('../models/ActivityLog');

const router = express.Router();

// Middleware to check if user is admin
const requireAdmin = (req, res, next) => {
  if (req.user.role !== 'admin') {
    return res.status(403).json({ message: 'Admin access required' });
  }
  next();
};

// GET /api/admin/stats - Get admin statistics
router.get('/stats', requireAdmin, async (req, res) => {
  try {
    const totalUsers = await User.countDocuments();
    const adminUsers = await User.countDocuments({ role: 'admin' });
    const activeUsers = await User.countDocuments({ isActive: true });
    const bannedUsers = await User.countDocuments({ isBanned: true });
    const blockedUsers = await User.countDocuments({ isBlocked: true });

    // Calculate today's messages (users with dailyMessages > 0)
    const todayMessages = await User.aggregate([
      { $match: { dailyMessages: { $gt: 0 } } },
      { $group: { _id: null, total: { $sum: '$dailyMessages' } } }
    ]);

    const messagesToday = todayMessages.length > 0 ? todayMessages[0].total : 0;

    // Count healthy Gemini keys
    const healthyKeys = await GeminiKey.countDocuments({ isActive: true });

    // Mock Gemini API calls for now (would need actual tracking)
    const geminiCalls = 0;

    const stats = {
      users: totalUsers,
      adminUsers: adminUsers,
      activeUsers: activeUsers,
      bannedUsers: bannedUsers,
      blockedUsers: blockedUsers,
      messagesToday: messagesToday,
      geminiCalls: geminiCalls,
      healthyKeys: healthyKeys
    };

    res.json(stats);

  } catch (error) {
    console.error('Get stats error:', error);
    res.status(500).json({ message: 'Internal server error' });
  }
});

// GET /api/admin/users - Get all users
router.get('/users', requireAdmin, async (req, res) => {
  try {
    const page = parseInt(req.query.page) || 1;
    const limit = parseInt(req.query.limit) || 10;
    const skip = (page - 1) * limit;

    const users = await User.find({})
      .select('-password')
      .skip(skip)
      .limit(limit)
      .sort({ createdAt: -1 });

    const total = await User.countDocuments();

    res.json({
      users,
      pagination: {
        page,
        limit,
        total,
        pages: Math.ceil(total / limit)
      }
    });

  } catch (error) {
    console.error('Get users error:', error);
    res.status(500).json({ message: 'Internal server error' });
  }
});

// PATCH /api/admin/users/:id - Update user
router.patch('/users/:id', requireAdmin, async (req, res) => {
  try {
    const { role, isActive, isBanned, isBlocked, resetCounter, name, email } = req.body;

    const updateData = {};
    if (role !== undefined) updateData.role = role;
    if (isActive !== undefined) updateData.isActive = isActive;
    if (isBanned !== undefined) updateData.isBanned = isBanned;
    if (isBlocked !== undefined) updateData.isBlocked = isBlocked;
    if (name !== undefined) updateData.name = name;
    if (email !== undefined) updateData.email = email;
    if (resetCounter) updateData.dailyMessages = 0;

    const user = await User.findByIdAndUpdate(
      req.params.id,
      updateData,
      { new: true }
    ).select('-password');

    if (!user) {
      return res.status(404).json({ message: 'User not found' });
    }

    // Log admin action
    let action = 'user_update';
    let message = 'Admin updated user information';
    if (isBanned === true) {
      action = 'user_ban';
      message = 'Admin banned user';
    } else if (isBanned === false) {
      action = 'user_unban';
      message = 'Admin unbanned user';
    } else if (isBlocked === true) {
      action = 'user_block';
      message = 'Admin blocked user';
    } else if (isBlocked === false) {
      action = 'user_unblock';
      message = 'Admin unblocked user';
    }

    await ActivityLog.logActivity({
      userId: req.user.userId,
      action: action,
      message: message,
      details: {
        targetUserId: user._id,
        targetUserEmail: user.email,
        changes: updateData
      },
      ipAddress: req.ip,
      userAgent: req.get('User-Agent'),
      level: 'info'
    });

    res.json({
      message: 'User updated successfully',
      user
    });

  } catch (error) {
    console.error('Update user error:', error);
    res.status(500).json({ message: 'Internal server error' });
  }
});

// DELETE /api/admin/users/:id - Delete user
router.delete('/users/:id', requireAdmin, async (req, res) => {
  try {
    const user = await User.findByIdAndDelete(req.params.id);

    if (!user) {
      return res.status(404).json({ message: 'User not found' });
    }

    // Log admin action
    await ActivityLog.logActivity({
      userId: req.user.userId,
      action: 'user_delete',
      message: 'Admin deleted user account',
      details: {
        deletedUserId: user._id,
        deletedUserEmail: user.email,
        deletedUserName: user.name
      },
      ipAddress: req.ip,
      userAgent: req.get('User-Agent'),
      level: 'warning'
    });

    res.json({ message: 'User deleted successfully' });

  } catch (error) {
    console.error('Delete user error:', error);
    res.status(500).json({ message: 'Internal server error' });
  }
});

// ===== GEMINI KEYS MANAGEMENT =====

// GET /api/admin/gemini-keys - Get all Gemini keys
router.get('/gemini-keys', requireAdmin, async (req, res) => {
  try {
    const keys = await GeminiKey.find({})
      .select('-key') // Don't send the actual key
      .sort({ createdAt: -1 });

    res.json(keys);

  } catch (error) {
    console.error('Get Gemini keys error:', error);
    res.status(500).json({ message: 'Internal server error' });
  }
});

// POST /api/admin/gemini-keys - Add new Gemini key
router.post('/gemini-keys', requireAdmin, async (req, res) => {
  try {
    const { name, key } = req.body;

    if (!name || !key) {
      return res.status(400).json({ message: 'Name and key are required' });
    }

    const newKey = new GeminiKey({
      name: name.trim(),
      key: key.trim()
    });

    await newKey.save();

    // Log admin action
    await ActivityLog.logActivity({
      userId: req.user.userId,
      action: 'api_key_added',
      message: 'Admin added new Gemini API key',
      details: {
        keyName: name.trim(),
        keyId: newKey._id
      },
      ipAddress: req.ip,
      userAgent: req.get('User-Agent'),
      level: 'info'
    });

    // Return without the actual key for security
    const response = newKey.toObject();
    delete response.key;

    res.status(201).json({
      message: 'Gemini key added successfully',
      key: response
    });

  } catch (error) {
    console.error('Add Gemini key error:', error);
    if (error.code === 11000) {
      res.status(400).json({ message: 'Key name already exists' });
    } else {
      res.status(500).json({ message: 'Internal server error' });
    }
  }
});

// PATCH /api/admin/gemini-keys/:id - Update Gemini key
router.patch('/gemini-keys/:id', requireAdmin, async (req, res) => {
  try {
    const { name, key, isActive } = req.body;

    const updateData = {};
    if (name !== undefined) updateData.name = name.trim();
    if (key !== undefined) updateData.key = key.trim();
    if (isActive !== undefined) updateData.isActive = isActive;

    const updatedKey = await GeminiKey.findByIdAndUpdate(
      req.params.id,
      updateData,
      { new: true }
    ).select('-key');

    if (!updatedKey) {
      return res.status(404).json({ message: 'Gemini key not found' });
    }

    res.json({
      message: 'Gemini key updated successfully',
      key: updatedKey
    });

  } catch (error) {
    console.error('Update Gemini key error:', error);
    res.status(500).json({ message: 'Internal server error' });
  }
});

// DELETE /api/admin/gemini-keys/:id - Delete Gemini key
router.delete('/gemini-keys/:id', requireAdmin, async (req, res) => {
  try {
    const key = await GeminiKey.findByIdAndDelete(req.params.id);

    if (!key) {
      return res.status(404).json({ message: 'Gemini key not found' });
    }

    res.json({ message: 'Gemini key deleted successfully' });

  } catch (error) {
    console.error('Delete Gemini key error:', error);
    res.status(500).json({ message: 'Internal server error' });
  }
});

// ===== SYSTEM SETTINGS MANAGEMENT =====

// GET /api/admin/settings - Get system settings
router.get('/settings', requireAdmin, async (req, res) => {
  try {
    const settings = await SystemSetting.find({});
    const settingsObj = {};

    settings.forEach(setting => {
      settingsObj[setting.key] = setting.value;
    });

    // Default settings if not found
    const defaultSettings = {
      dailyLimit: settingsObj.dailyLimit || 100,
      maintenanceMode: settingsObj.maintenanceMode || false,
      banner: settingsObj.banner || '',
      ...settingsObj
    };

    res.json(defaultSettings);

  } catch (error) {
    console.error('Get settings error:', error);
    res.status(500).json({ message: 'Internal server error' });
  }
});

// PATCH /api/admin/settings - Update system settings
router.patch('/settings', requireAdmin, async (req, res) => {
  try {
    const { dailyLimit, maintenanceMode, banner } = req.body;

    const updates = [];

    if (dailyLimit !== undefined) {
      updates.push({
        updateOne: {
          filter: { key: 'dailyLimit' },
          update: {
            key: 'dailyLimit',
            value: parseInt(dailyLimit),
            type: 'number',
            description: 'Daily message limit per user'
          },
          upsert: true
        }
      });
    }

    if (maintenanceMode !== undefined) {
      updates.push({
        updateOne: {
          filter: { key: 'maintenanceMode' },
          update: {
            key: 'maintenanceMode',
            value: maintenanceMode,
            type: 'boolean',
            description: 'System maintenance mode'
          },
          upsert: true
        }
      });
    }

    if (banner !== undefined) {
      updates.push({
        updateOne: {
          filter: { key: 'banner' },
          update: {
            key: 'banner',
            value: banner,
            type: 'string',
            description: 'System banner message'
          },
          upsert: true
        }
      });
    }

    if (updates.length > 0) {
      await SystemSetting.bulkWrite(updates);
    }

    // Log admin action
    await ActivityLog.logActivity({
      userId: req.user.userId,
      action: 'settings_updated',
      message: 'Admin updated system settings',
      details: {
        updatedSettings: { dailyLimit, maintenanceMode, banner }
      },
      ipAddress: req.ip,
      userAgent: req.get('User-Agent'),
      level: 'info'
    });

    res.json({ message: 'Settings updated successfully' });

  } catch (error) {
    console.error('Update settings error:', error);
    res.status(500).json({ message: 'Internal server error' });
  }
});

// ===== ACTIVITY LOGS MANAGEMENT =====

// GET /api/admin/logs - Get activity logs
router.get('/logs', requireAdmin, async (req, res) => {
  try {
    const page = parseInt(req.query.page) || 1;
    const limit = parseInt(req.query.limit) || 50;
    const skip = (page - 1) * limit;

    // Filters
    const filter = {};
    if (req.query.action) filter.action = req.query.action;
    if (req.query.level) filter.level = req.query.level;
    if (req.query.userId) filter.userId = req.query.userId;

    // Date range filter
    if (req.query.startDate || req.query.endDate) {
      filter.createdAt = {};
      if (req.query.startDate) filter.createdAt.$gte = new Date(req.query.startDate);
      if (req.query.endDate) filter.createdAt.$lte = new Date(req.query.endDate);
    }

    const logs = await ActivityLog.find(filter)
      .populate('userId', 'name email')
      .sort({ createdAt: -1 })
      .skip(skip)
      .limit(limit);

    const total = await ActivityLog.countDocuments(filter);

    res.json({
      logs,
      pagination: {
        page,
        limit,
        total,
        pages: Math.ceil(total / limit)
      }
    });

  } catch (error) {
    console.error('Get logs error:', error);
    res.status(500).json({ message: 'Internal server error' });
  }
});

// GET /api/admin/logs/stats - Get log statistics
router.get('/logs/stats', requireAdmin, async (req, res) => {
  try {
    const today = new Date();
    today.setHours(0, 0, 0, 0);
    const tomorrow = new Date(today);
    tomorrow.setDate(tomorrow.getDate() + 1);

    const [
      totalLogs,
      todayLogs,
      errorLogs,
      userActions,
      adminActions
    ] = await Promise.all([
      ActivityLog.countDocuments(),
      ActivityLog.countDocuments({ createdAt: { $gte: today, $lt: tomorrow } }),
      ActivityLog.countDocuments({ level: { $in: ['error', 'critical'] } }),
      ActivityLog.countDocuments({ action: { $regex: '^user_' } }),
      ActivityLog.countDocuments({ action: { $regex: '^admin_' } })
    ]);

    res.json({
      totalLogs,
      todayLogs,
      errorLogs,
      userActions,
      adminActions
    });

  } catch (error) {
    console.error('Get log stats error:', error);
    res.status(500).json({ message: 'Internal server error' });
  }
});

// DELETE /api/admin/logs - Clear old logs (older than specified days)
router.delete('/logs', requireAdmin, async (req, res) => {
  try {
    const days = parseInt(req.query.days) || 30; // Default 30 days
    const cutoffDate = new Date();
    cutoffDate.setDate(cutoffDate.getDate() - days);

    const result = await ActivityLog.deleteMany({
      createdAt: { $lt: cutoffDate }
    });

    res.json({
      message: `Deleted ${result.deletedCount} logs older than ${days} days`
    });

  } catch (error) {
    console.error('Clear logs error:', error);
    res.status(500).json({ message: 'Internal server error' });
  }
});

module.exports = router;