#!/usr/bin/env node

const fs = require('fs');
const path = require('path');

console.log('🚀 SensCoder Backend Setup');
console.log('==========================\n');

// Check if .env file exists
const envPath = path.join(__dirname, '.env');
if (!fs.existsSync(envPath)) {
  console.log('❌ .env file not found!');
  process.exit(1);
}

// Read current .env file
let envContent = fs.readFileSync(envPath, 'utf8');

// Check if GEMINI_API_KEY is set
if (envContent.includes('GEMINI_API_KEY=your-gemini-api-key-here') ||
    !envContent.includes('GEMINI_API_KEY=')) {
  console.log('⚠️  GEMINI_API_KEY is not configured!');
  console.log('');
  console.log('To set up your Gemini API key:');
  console.log('1. Go to https://makersuite.google.com/app/apikey');
  console.log('2. Create a new API key');
  console.log('3. Copy the API key');
  console.log('4. Replace "your-gemini-api-key-here" in the .env file with your actual key');
  console.log('');
  console.log('Example:');
  console.log('GEMINI_API_KEY=AIzaSyD...your-actual-key-here');
  console.log('');
} else {
  console.log('GEMINI_API_KEY is configured');
}

// Check other required environment variables
const requiredVars = ['MONGODB_URI', 'JWT_SECRET', 'PORT'];
const missingVars = [];

requiredVars.forEach(varName => {
  if (!envContent.includes(`${varName}=`)) {
    missingVars.push(varName);
  }
});

if (missingVars.length > 0) {
  console.log(`❌ Missing required environment variables: ${missingVars.join(', ')}`);
} else {
  console.log('All required environment variables are set');
}

console.log('');
console.log('Setup complete! Run "npm start" to start the server.');