import express from 'express';
import authController from '../controllers/auth.controller';
import { authenticate } from '../../../middleware/authMiddleware';

const router = express.Router();

/**
 * @route POST /api/auth/register
 * @desc Register a new user
 * @access Public
 */
router.post('/register', authController.register);

/**
 * @route POST /api/auth/login
 * @desc Login a user
 * @access Public
 */
router.post('/login', authController.login);

/**
 * @route GET /api/auth/profile
 * @desc Get user profile
 * @access Private
 */
router.get('/profile', authenticate, authController.getProfile);

export default router;