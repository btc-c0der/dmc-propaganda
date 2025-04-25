import { Request, Response, NextFunction } from 'express';
import config from '../config';

interface AppError extends Error {
  statusCode?: number;
  status?: string;
  isOperational?: boolean;
}

/**
 * Global error handler middleware
 */
export const errorHandler = (
  err: AppError,
  req: Request,
  res: Response,
  next: NextFunction
) => {
  const statusCode = err.statusCode || 500;
  const status = err.status || 'error';

  // Only log detailed error in development
  const errorResponse = {
    status,
    message: err.message,
    ...(config.isDevelopment && { stack: err.stack }),
    ...(config.isDevelopment && { error: err }),
  };

  // Log the error
  console.error(`[ERROR] ${req.method} ${req.path}:`, err);

  return res.status(statusCode).json(errorResponse);
};

/**
 * Custom application error class
 */
export class ApiError extends Error {
  statusCode: number;
  status: string;
  isOperational: boolean;

  constructor(statusCode: number, message: string, isOperational = true) {
    super(message);
    this.statusCode = statusCode;
    this.status = `${statusCode}`.startsWith('4') ? 'fail' : 'error';
    this.isOperational = isOperational;

    Error.captureStackTrace(this, this.constructor);
  }
}