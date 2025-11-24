# SensCoder Backend

A Node.js/Express backend for the SensCoder application with AI chat capabilities, user management, and MCP server integration.

## Features

- 🔐 JWT Authentication with secure password hashing
- 🤖 Google Gemini AI integration for chat functionality
- 👥 User management with admin panel
- 🔑 API key management for AI services
- 📊 Usage tracking and rate limiting
- 🛡️ Admin controls (ban, block, message limits)
- 🔌 MCP server integration
- 📱 RESTful API design

## Setup

### Prerequisites

- Node.js 16+
- MongoDB
- Google Gemini API key

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd senscoder-backend
   ```

2. **Install dependencies**
   ```bash
   npm install
   ```

3. **Environment Setup**
   ```bash
   cp .env.example .env
   # Edit .env file with your configuration
   ```

4. **Configure Environment Variables**
   ```env
   MONGODB_URI=mongodb://localhost:27017/senscoder
   JWT_SECRET=your-super-secret-jwt-key-change-this-in-production
   PORT=4000
   FRONTEND_URL=http://localhost:5173
   GEMINI_API_KEY=your-gemini-api-key-here
   ```

5. **Get Gemini API Key**
   - Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
   - Create a new API key
   - Add it to your `.env` file

6. **Run Setup Script**
   ```bash
   npm run setup
   ```

7. **Start the Server**
   ```bash
   # Development
   npm run dev

   # Production
   npm start
   ```

## API Endpoints

### Authentication
- `POST /api/auth/signup` - User registration
- `POST /api/auth/login` - User login
- `GET /api/auth/me` - Get current user info

### Chat
- `POST /api/chat` - Send message to AI (requires auth)

### Settings
- `GET /api/settings` - Get user settings (requires auth)
- `PUT /api/settings` - Update user settings (requires auth)

### Admin (requires admin role)
- `GET /api/admin/stats` - Get admin statistics
- `GET /api/admin/users` - List users with pagination
- `PATCH /api/admin/users/:id` - Update user
- `DELETE /api/admin/users/:id` - Delete user
- `GET /api/admin/gemini-keys` - List Gemini API keys
- `POST /api/admin/gemini-keys` - Add new Gemini key
- `PATCH /api/admin/gemini-keys/:id` - Update Gemini key
- `DELETE /api/admin/gemini-keys/:id` - Delete Gemini key
- `GET /api/admin/settings` - Get system settings
- `PATCH /api/admin/settings` - Update system settings

### Integrations
- `GET /api/integrations/status` - Get integration status

### MCP Server
- `POST /api/mcp/start` - Start MCP server
- `POST /api/mcp/stop` - Stop MCP server
- `GET /api/mcp/status` - Get MCP server status

## Database Models

### User
- Authentication fields (email, password, name)
- Role-based access (user/admin)
- API settings and preferences
- Usage tracking (daily messages, last activity)
- Admin controls (ban, block status)

### GeminiKey
- API key storage with encryption
- Usage tracking and limits
- Active/inactive status

### SystemSetting
- Global application settings
- Maintenance mode, daily limits, banners

## Security Features

- Password hashing with bcrypt
- JWT token authentication
- Rate limiting on API endpoints
- Input validation and sanitization
- Admin role verification
- API key encryption

## Development

### Scripts
- `npm run dev` - Start development server with nodemon
- `npm start` - Start production server
- `npm run setup` - Check environment configuration

### Project Structure
```
backend/
├── models/          # Database models
├── routes/          # API route handlers
├── server.js        # Main application file
├── setup.js         # Configuration checker
├── .env             # Environment variables
└── package.json     # Dependencies and scripts
```

## Error Handling

The API provides comprehensive error handling with appropriate HTTP status codes:

- `400` - Bad Request (invalid input)
- `401` - Unauthorized (missing/invalid token)
- `403` - Forbidden (insufficient permissions)
- `404` - Not Found
- `429` - Too Many Requests (rate limited)
- `500` - Internal Server Error

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

MIT License - see LICENSE file for details