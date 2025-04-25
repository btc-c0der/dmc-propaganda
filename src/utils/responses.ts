import { Response } from 'express';
import { ResponseResult, Pagination } from '../interfaces/common';

/**
 * Helper class for standardizing API responses
 */
export class ApiResponse {
  /**
   * Send a success response
   */
  static success<T>(
    res: Response,
    data?: T,
    message = 'Operation successful',
    statusCode = 200,
    pagination?: Pagination
  ): Response {
    const response: ResponseResult<T> = {
      success: true,
      message,
      data,
    };

    if (pagination) {
      response.pagination = pagination;
    }

    return res.status(statusCode).json(response);
  }

  /**
   * Send an error response
   */
  static error(
    res: Response,
    message = 'An error occurred',
    statusCode = 500,
    error?: any
  ): Response {
    const response: ResponseResult<null> = {
      success: false,
      message,
      error,
    };

    return res.status(statusCode).json(response);
  }

  /**
   * Send a not found response
   */
  static notFound(
    res: Response,
    message = 'Resource not found'
  ): Response {
    return ApiResponse.error(res, message, 404);
  }

  /**
   * Send an unauthorized response
   */
  static unauthorized(
    res: Response,
    message = 'Unauthorized access'
  ): Response {
    return ApiResponse.error(res, message, 401);
  }

  /**
   * Send a forbidden response
   */
  static forbidden(
    res: Response,
    message = 'Access forbidden'
  ): Response {
    return ApiResponse.error(res, message, 403);
  }

  /**
   * Send a bad request response
   */
  static badRequest(
    res: Response,
    message = 'Bad request',
    error?: any
  ): Response {
    return ApiResponse.error(res, message, 400, error);
  }
}