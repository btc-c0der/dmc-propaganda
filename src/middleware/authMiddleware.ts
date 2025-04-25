import { Request, Response, NextFunction } from 'express';
import jwt from 'jsonwebtoken';
import config from '../config';
import { ApiError } from './errorHandler';
import { ApiResponse } from '../utils/responses';

// Extend Express Request interface to include user property
declare global {
  namespace Express {
    interface Request {
      user?: any;
    }
  }
}

/**
 * Middleware to protect routes - verifies JWT token
 */
export const authenticate = async (
  req: Request,
  res: Response,
  next: NextFunction
) => {
  try {
    // Get token from Authorization header
    const authHeader = req.headers.authorization;
    
    if (!authHeader || !authHeader.startsWith('Bearer ')) {
      return ApiResponse.unauthorized(res, 'Authentication required');
    }

    const token = authHeader.split(' ')[1];
    
    // Verify token
    const decoded = jwt.verify(token, config.jwt.secret) as any;
    
    // Attach user to request object
    req.user = decoded;
    next();
  } catch (error) {
    if (error instanceof jwt.JsonWebTokenError) {
      return ApiResponse.unauthorized(res, 'Invalid or expired token');
    }
    next(new ApiError(500, 'Authentication error'));
  }
};

/**
 * Middleware to check if the user has the required role
 */
export const authorize = (roles: string[]) => {
  return (req: Request, res: Response, next: NextFunction) => {
    if (!req.user) {
      return ApiResponse.unauthorized(res, 'Authentication required');
    }

    if (!roles.includes(req.user.role)) {
      return ApiResponse.forbidden(res, 'You do not have permission to perform this action');
    }

    next();
  };
};