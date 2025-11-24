const mongoose = require('mongoose');
const User = require('./models/User');
require('dotenv').config();

async function createAdmin() {
  try {
    // Connect to MongoDB
    await mongoose.connect(process.env.MONGODB_URI);
    console.log('Connected to MongoDB');

    // Check if admin already exists
    const existingAdmin = await User.findOne({ email: 'omchoksi@gmail.com' });
    if (existingAdmin) {
      console.log('⚠️  Admin user already exists');
      process.exit(0);
    }

    // Create admin user
    const admin = new User({
      email: 'omchoksi@gmail.com',
      password: 'admin123', // Will be hashed by pre-save middleware
      name: 'Admin User',
      role: 'admin'
    });

    await admin.save();
    console.log('Admin user created successfully!');
    console.log('📧 Email: omchoksi@gmail.com');
    console.log('🔑 Password: admin123');

  } catch (error) {
    console.error('❌ Error creating admin:', error);
  } finally {
    await mongoose.connection.close();
    process.exit(0);
  }
}

createAdmin();