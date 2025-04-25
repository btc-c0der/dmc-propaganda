import express from 'express';
import helmet from 'helmet';
import cors from 'cors';
import compression from 'compression';
import config from './config';
import database from './config/database';
import { errorHandler } from './middleware/errorHandler';
import { notFoundHandler } from './middleware/notFoundHandler';
import { requestLogger } from './middleware/requestLogger';

// Import module routes
import authRoutes from './modules/auth/routes';
import clientRoutes from './modules/client/routes';
import campaignRoutes from './modules/campaign/routes';
import mediaRoutes from './modules/media/routes';
import analyticsRoutes from './modules/analytics/routes';

// Initialize express app
const app = express();

// Apply middleware
app.use(helmet());
app.use(cors({
  origin: config.cors.origin,
  credentials: true,
}));
app.use(compression());
app.use(express.json());
app.use(express.urlencoded({ extended: true }));
app.use(requestLogger);

// API Routes
app.use('/api/auth', authRoutes);
app.use('/api/clients', clientRoutes);
app.use('/api/campaigns', campaignRoutes);
app.use('/api/media', mediaRoutes);
app.use('/api/analytics', analyticsRoutes);

// Base route
app.get('/', (req, res) => {
  res.json({
    message: 'DMC Propaganda API',
    version: '1.0.0',
    environment: config.env,
  });
});

// Error handling
app.use(notFoundHandler);
app.use(errorHandler);

// Connect to database and start server
const startServer = async (): Promise<void> => {
  try {
    await database.connect();
    
    const server = app.listen(config.port, () => {
      console.log(`Server running on port ${config.port} in ${config.env} mode`);
    });

    // Handle graceful shutdown
    process.on('SIGTERM', () => {
      console.log('SIGTERM received, shutting down gracefully');
      server.close(async () => {
        await database.disconnect();
        console.log('Process terminated');
        process.exit(0);
      });
    });

  } catch (error) {
    console.error('Failed to start server:', error);
    process.exit(1);
  }
};

startServer();

export default app;