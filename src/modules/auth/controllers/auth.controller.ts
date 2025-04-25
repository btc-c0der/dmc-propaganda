import { Request, Response, NextFunction } from 'express';
import authService from '../services/auth.service';
import { ApiResponse } from '../../../utils/responses';

class AuthController {
  /**
   * Register a new user
   * @route POST /api/auth/register
   */
  async register(req: Request, res: Response, next: NextFunction) {
    try {
      const userData = req.body;
      const result = await authService.register(userData);
      
      return ApiResponse.success(res, result, 'User registered successfully', 201);
    } catch (error) {
      next(error);
    }
  }

  /**
   * Login a user
   * @route POST /api/auth/login
   */
  async login(req: Request, res: Response, next: NextFunction) {
    try {
      const { email, password } = req.body;
      
      const result = await authService.login({ email, password });
      
      return ApiResponse.success(res, result, 'Login successful');
    } catch (error) {
      next(error);
    }
  }

  /**
   * Get user profile
   * @route GET /api/auth/profile
   */
  async getProfile(req: Request, res: Response, next: NextFunction) {
    try {
      const userId = req.user.id; // From auth middleware
      const user = await authService.getProfile(userId);
      
      return ApiResponse.success(res, user, 'User profile retrieved successfully');
    } catch (error) {
      next(error);
    }
  }
}

export default new AuthController();