import dotenv from 'dotenv';
import path from 'path';

// Load environment variables from .env file
dotenv.config();

const config = {
  env: process.env.NODE_ENV || 'development',
  port: parseInt(process.env.PORT || '3000', 10),
  mongo: {
    uri: process.env.MONGODB_URI || 'mongodb://localhost:27017/dmc-propaganda',
  },
  jwt: {
    secret: process.env.JWT_SECRET || 'default_jwt_secret_key',
    expiration: process.env.JWT_EXPIRATION || '7d',
  },
  cors: {
    origin: process.env.CORS_ORIGIN || '*',
  },
  logs: {
    level: process.env.LOG_LEVEL || 'debug',
  },
  isDevelopment: process.env.NODE_ENV !== 'production',
  isProduction: process.env.NODE_ENV === 'production',
  isTest: process.env.NODE_ENV === 'test',
};

export default config;