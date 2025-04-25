import mongoose from 'mongoose';
import authService from '../../../modules/auth/services/auth.service';
import User from '../../../modules/auth/models/user.model';
import { ApiError } from '../../../middleware/errorHandler';

// Mock the User model
jest.mock('../../../modules/auth/models/user.model');

describe('Auth Service', () => {
  // Clean up after tests
  afterEach(() => {
    jest.resetAllMocks();
  });

  afterAll(() => {
    jest.clearAllMocks();
  });

  describe('register', () => {
    it('should successfully register a new user', async () => {
      // Mock user data
      const userData = {
        name: 'Test User',
        email: 'test@example.com',
        password: 'password123',
      };

      // Mock User.findOne to return null (user doesn't exist)
      (User.findOne as jest.Mock).mockResolvedValue(null);

      // Mock User.create to return a new user
      const mockUser = {
        _id: new mongoose.Types.ObjectId(),
        name: userData.name,
        email: userData.email,
        role: 'user',
      };
      (User.create as jest.Mock).mockResolvedValue(mockUser);

      // Call the register function
      const result = await authService.register(userData);

      // Assert User.findOne was called with the correct email
      expect(User.findOne).toHaveBeenCalledWith({ email: userData.email });
      
      // Assert User.create was called with the user data
      expect(User.create).toHaveBeenCalledWith({
        name: userData.name,
        email: userData.email,
        password: userData.password,
        role: 'user',
      });

      // Assert the function returns the expected result
      expect(result).toHaveProperty('user');
      expect(result).toHaveProperty('token');
      expect(result.user).toHaveProperty('name', userData.name);
      expect(result.user).toHaveProperty('email', userData.email);
      expect(result.token).toBeDefined();
    });

    it('should throw an error if user already exists', async () => {
      // Mock user data
      const userData = {
        name: 'Test User',
        email: 'existing@example.com',
        password: 'password123',
      };

      // Mock User.findOne to return an existing user
      (User.findOne as jest.Mock).mockResolvedValue({
        _id: new mongoose.Types.ObjectId(),
        email: userData.email,
      });

      // Assert that the function throws an error
      await expect(authService.register(userData)).rejects.toThrow(ApiError);
      await expect(authService.register(userData)).rejects.toThrow('Email already in use');
    });
  });

  describe('login', () => {
    it('should successfully login a user with valid credentials', async () => {
      // Mock login credentials
      const credentials = {
        email: 'test@example.com',
        password: 'password123',
      };

      // Mock user with comparePassword method
      const mockUser = {
        _id: new mongoose.Types.ObjectId(),
        name: 'Test User',
        email: credentials.email,
        role: 'user',
        lastLogin: null,
        isActive: true,
        comparePassword: jest.fn().mockResolvedValue(true),
        save: jest.fn().mockResolvedValue(true),
      };

      // Mock User.findOne to return the mock user
      (User.findOne as jest.Mock).mockImplementation(() => ({
        select: jest.fn().mockResolvedValue(mockUser),
      }));

      // Call the login function
      const result = await authService.login(credentials);

      // Assert that the correct methods were called
      expect(User.findOne).toHaveBeenCalledWith({ email: credentials.email });
      expect(mockUser.comparePassword).toHaveBeenCalledWith(credentials.password);
      expect(mockUser.save).toHaveBeenCalled();

      // Assert the function returns the expected result
      expect(result).toHaveProperty('user');
      expect(result).toHaveProperty('token');
      expect(result.user).toHaveProperty('name', mockUser.name);
      expect(result.user).toHaveProperty('email', mockUser.email);
      expect(result.token).toBeDefined();
    });

    it('should throw an error if user is not found', async () => {
      // Mock login credentials
      const credentials = {
        email: 'nonexistent@example.com',
        password: 'password123',
      };

      // Mock User.findOne to return null (user doesn't exist)
      (User.findOne as jest.Mock).mockImplementation(() => ({
        select: jest.fn().mockResolvedValue(null),
      }));

      // Assert that the function throws an error
      await expect(authService.login(credentials)).rejects.toThrow(ApiError);
      await expect(authService.login(credentials)).rejects.toThrow('Invalid credentials');
    });

    it('should throw an error if user account is inactive', async () => {
      // Mock login credentials
      const credentials = {
        email: 'inactive@example.com',
        password: 'password123',
      };

      // Mock inactive user
      const mockUser = {
        _id: new mongoose.Types.ObjectId(),
        email: credentials.email,
        isActive: false,
      };

      // Mock User.findOne to return inactive user
      (User.findOne as jest.Mock).mockImplementation(() => ({
        select: jest.fn().mockResolvedValue(mockUser),
      }));

      // Assert that the function throws an error
      await expect(authService.login(credentials)).rejects.toThrow(ApiError);
      await expect(authService.login(credentials)).rejects.toThrow('Your account has been deactivated');
    });

    it('should throw an error if password is incorrect', async () => {
      // Mock login credentials
      const credentials = {
        email: 'test@example.com',
        password: 'wrongPassword',
      };

      // Mock user with comparePassword method that returns false
      const mockUser = {
        _id: new mongoose.Types.ObjectId(),
        email: credentials.email,
        isActive: true,
        comparePassword: jest.fn().mockResolvedValue(false),
      };

      // Mock User.findOne to return the mock user
      (User.findOne as jest.Mock).mockImplementation(() => ({
        select: jest.fn().mockResolvedValue(mockUser),
      }));

      // Assert that the function throws an error
      await expect(authService.login(credentials)).rejects.toThrow(ApiError);
      await expect(authService.login(credentials)).rejects.toThrow('Invalid credentials');
    });
  });
});