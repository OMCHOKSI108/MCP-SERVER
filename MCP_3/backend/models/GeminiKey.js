const mongoose = require('mongoose');

const geminiKeySchema = new mongoose.Schema({
  name: {
    type: String,
    required: true,
    trim: true
  },
  key: {
    type: String,
    required: true,
    trim: true
  },
  dailyCalls: {
    type: Number,
    default: 0
  },
  isActive: {
    type: Boolean,
    default: true
  },
  lastUsedAt: {
    type: Date,
    default: null
  },
  createdAt: {
    type: Date,
    default: Date.now
  }
});

// Index for performance
geminiKeySchema.index({ isActive: 1, createdAt: -1 });

module.exports = mongoose.model('GeminiKey', geminiKeySchema);