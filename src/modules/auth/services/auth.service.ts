import jwt from 'jsonwebtoken';
import User, { IUser } from '../models/user.model';
import { ApiError } from '../../../middleware/errorHandler';
import config from '../../../config';

export interface AuthResponse {
  user: Partial<IUser>;
  token: string;
}

export interface RegisterInput {
  name: string;
  email: string;
  password: string;
  role?: 'admin' | 'manager' | 'user';
}

export interface LoginInput {
  email: string;
  password: string;
}

/**
 * Authentication Service
 */
class AuthService {
  /**
   * Register a new user
   */
  async register(userData: RegisterInput): Promise<AuthResponse> {
    // Check if user already exists
    const existingUser = await User.findOne({ email: userData.email });
    if (existingUser) {
      throw new ApiError(400, 'Email already in use');
    }

    // Create new user
    const user = await User.create({
      ...userData,
      role: userData.role || 'user', // Default role is user
    });

    // Generate JWT token
    const token = this.generateToken(user);

    // Remove sensitive data before returning
    const userWithoutSensitiveData = {
      _id: user._id,
      name: user.name,
      email: user.email,
      role: user.role,
    };

    return {
      user: userWithoutSensitiveData,
      token,
    };
  }

  /**
   * Login a user
   */
  async login(credentials: LoginInput): Promise<AuthResponse> {
    // Find user and include password for comparison
    const user = await User.findOne({ email: credentials.email }).select('+password');
    
    if (!user) {
      throw new ApiError(401, 'Invalid credentials');
    }

    // Check if user is active
    if (!user.isActive) {
      throw new ApiError(401, 'Your account has been deactivated');
    }

    // Check password
    const isPasswordValid = await user.comparePassword(credentials.password);
    if (!isPasswordValid) {
      throw new ApiError(401, 'Invalid credentials');
    }

    // Update last login timestamp
    user.lastLogin = new Date();
    await user.save();

    // Generate JWT token
    const token = this.generateToken(user);

    // Remove sensitive data before returning
    const userWithoutSensitiveData = {
      _id: user._id,
      name: user.name,
      email: user.email,
      role: user.role,
      lastLogin: user.lastLogin,
    };

    return {
      user: userWithoutSensitiveData,
      token,
    };
  }

  /**
   * Get user profile by ID
   */
  async getProfile(userId: string): Promise<IUser | null> {
    const user = await User.findById(userId);
    
    if (!user) {
      throw new ApiError(404, 'User not found');
    }

    return user;
  }

  /**
   * Generate a JWT token for a user
   */
  private generateToken(user: IUser): string {
    return jwt.sign(
      {
        id: user._id,
        email: user.email,
        role: user.role,
      },
      config.jwt.secret,
      { expiresIn: config.jwt.expiration }
    );
  }
}

export default new AuthService();