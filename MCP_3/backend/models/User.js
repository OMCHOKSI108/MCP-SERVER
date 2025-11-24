const mongoose = require('mongoose');
const bcrypt = require('bcryptjs');

const userSchema = new mongoose.Schema({
  email: {
    type: String,
    required: true,
    unique: true,
    lowercase: true,
    trim: true
  },
  password: {
    type: String,
    required: true
  },
  name: {
    type: String,
    required: true,
    trim: true
  },
  role: {
    type: String,
    enum: ['user', 'admin'],
    default: 'user'
  },
  avatar: String,
  isActive: {
    type: Boolean,
    default: true
  },
  // API settings
  apiProvider: {
    type: String,
    enum: ['gemini', 'openai', 'anthropic', 'groq', 'openrouter', 'ollama'],
    default: 'gemini'
  },
  apiKey: {
    type: String,
    select: false // Don't include in regular queries for security
  },
  hasApiKey: {
    type: Boolean,
    default: false
  },
  // User preferences
  theme: {
    type: String,
    enum: ['light', 'dark'],
    default: 'dark'
  },
  language: {
    type: String,
    default: 'en'
  },
  notifications: {
    type: Boolean,
    default: true
  },
  // Admin fields
  dailyMessages: {
    type: Number,
    default: 0
  },
  isBanned: {
    type: Boolean,
    default: false
  },
  isBlocked: {
    type: Boolean,
    default: false
  },
  lastActivity: {
    type: Date,
    default: null
  }
}, {
  timestamps: true
});

// Hash password before saving
userSchema.pre('save', async function(next) {
  if (!this.isModified('password')) return next();

  try {
    const salt = await bcrypt.genSalt(12);
    this.password = await bcrypt.hash(this.password, salt);
    next();
  } catch (error) {
    next(error);
  }
});

// Compare password method
userSchema.methods.comparePassword = async function(candidatePassword) {
  return bcrypt.compare(candidatePassword, this.password);
};

// Remove password from JSON output
userSchema.methods.toJSON = function() {
  const userObject = this.toObject();
  delete userObject.password;
  return userObject;
};

module.exports = mongoose.model('User', userSchema);