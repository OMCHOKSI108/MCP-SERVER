#!/usr/bin/env node

const http = require('http');

const BASE_URL = 'http://localhost:4000';

function makeRequest(path, options = {}) {
  return new Promise((resolve, reject) => {
    const url = new URL(path, BASE_URL + '/');
    const req = http.request(url, {
      method: options.method || 'GET',
      headers: options.headers || {}
    }, (res) => {
      let data = '';
      res.on('data', chunk => data += chunk);
      res.on('end', () => {
        try {
          const json = JSON.parse(data);
          resolve({ status: res.statusCode, data: json });
        } catch (e) {
          resolve({ status: res.statusCode, data });
        }
      });
    });

    req.on('error', reject);

    if (options.body) {
      req.write(JSON.stringify(options.body));
    }

    req.end();
  });
}

async function testAPI() {
  console.log('🧪 Testing SensCoder Backend API');
  console.log('=================================\n');

  try {
    // Test health check
    console.log('Testing health check...');
    const healthResponse = await makeRequest('/api/health');
    if (healthResponse.status === 200) {
      console.log('Health check passed:', healthResponse.data);
    } else {
      console.log('❌ Health check failed:', healthResponse);
    }

    // Test invalid auth on chat endpoint
    console.log('\nTesting authentication...');
    const chatResponse = await makeRequest('/api/chat', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: { messages: [{ content: 'Hello' }] }
    });

    if (chatResponse.status === 401) {
      console.log('Authentication properly required');
    } else {
      console.log('❌ Unexpected auth response:', chatResponse);
    }

    console.log('\n🎉 Basic API tests completed!');
    console.log('\nNext steps:');
    console.log('1. Set up your GEMINI_API_KEY in .env');
    console.log('2. Start the frontend: cd ../frontend && npm run dev');
    console.log('3. Test full authentication flow');

  } catch (error) {
    console.log('❌ API test failed:', error.message);
    if (error.code === 'ECONNREFUSED') {
      console.log('💡 Make sure the backend server is running: npm start');
    }
  }
}

testAPI();