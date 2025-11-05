const express = require('express');
const _ = require('lodash');

/**
 * Sample Express.js application
 * This demonstrates a basic REST API server
 */
class SampleApp {
    constructor() {
        this.app = express();
        this.setupMiddleware();
        this.setupRoutes();
    }

    /**
     * Configure middleware
     */
    setupMiddleware() {
        this.app.use(express.json());
        this.app.use(express.urlencoded({ extended: true }));
    }

    /**
     * Define API routes
     */
    setupRoutes() {
        // Health check endpoint
        this.app.get('/health', (req, res) => {
            res.json({ status: 'OK', timestamp: new Date().toISOString() });
        });

        // Users endpoint
        this.app.get('/api/users', (req, res) => {
            const users = [
                { id: 1, name: 'John Doe', email: 'john@example.com' },
                { id: 2, name: 'Jane Smith', email: 'jane@example.com' }
            ];
            res.json(users);
        });

        // Process data endpoint
        this.app.post('/api/process', (req, res) => {
            const { data } = req.body;
            const processed = _.map(data, item => ({
                ...item,
                processed: true,
                timestamp: new Date().toISOString()
            }));
            res.json({ result: processed });
        });
    }

    /**
     * Start the server
     */
    start(port = 3000) {
        this.app.listen(port, () => {
            console.log(`Server running on port ${port}`);
        });
    }
}

// Export for testing
module.exports = SampleApp;

// Start server if run directly
if (require.main === module) {
    const app = new SampleApp();
    app.start();
}