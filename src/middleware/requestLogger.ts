import { Request, Response, NextFunction } from 'express';
import config from '../config';

/**
 * Middleware to log all incoming requests
 */
export const requestLogger = (req: Request, res: Response, next: NextFunction) => {
  // Only log in development environment
  if (config.isDevelopment) {
    const start = Date.now();
    
    // Log request
    console.log(`[${new Date().toISOString()}] ${req.method} ${req.path}`);
    
    // Log request body if present and not sensitive data
    if (req.body && Object.keys(req.body).length > 0 && !isSensitiveRoute(req.path)) {
      console.log('Request body:', JSON.stringify(req.body, null, 2));
    }
    
    // Log response time when response is sent
    res.on('finish', () => {
      const duration = Date.now() - start;
      console.log(`[${new Date().toISOString()}] ${req.method} ${req.path} - ${res.statusCode} (${duration}ms)`);
    });
  }
  
  next();
};

/**
 * Check if the route is sensitive (e.g. auth routes) to avoid logging sensitive data
 */
const isSensitiveRoute = (path: string): boolean => {
  const sensitiveRoutes = ['/api/auth/login', '/api/auth/register', '/api/auth/reset-password'];
  return sensitiveRoutes.some(route => path.includes(route));
};