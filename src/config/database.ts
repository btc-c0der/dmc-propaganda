import mongoose from 'mongoose';
import config from './index';

/**
 * Database connection manager for MongoDB
 */
class Database {
  private static instance: Database;
  private isConnected: boolean = false;

  private constructor() {}

  public static getInstance(): Database {
    if (!Database.instance) {
      Database.instance = new Database();
    }
    return Database.instance;
  }

  /**
   * Connect to MongoDB
   */
  public async connect(): Promise<void> {
    if (this.isConnected) {
      console.log('MongoDB is already connected');
      return;
    }

    try {
      const options = {
        autoIndex: true,
      };

      await mongoose.connect(config.mongo.uri, options);
      this.isConnected = true;
      console.log('MongoDB connected successfully');
    } catch (error) {
      console.error('MongoDB connection error:', error);
      process.exit(1);
    }
  }

  /**
   * Disconnect from MongoDB
   */
  public async disconnect(): Promise<void> {
    if (!this.isConnected) {
      return;
    }

    try {
      await mongoose.disconnect();
      this.isConnected = false;
      console.log('MongoDB disconnected');
    } catch (error) {
      console.error('MongoDB disconnection error:', error);
      process.exit(1);
    }
  }
}

export default Database.getInstance();