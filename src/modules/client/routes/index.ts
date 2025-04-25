import express from 'express';
import clientController from '../controllers/client.controller';
import { authenticate, authorize } from '../../../middleware/authMiddleware';

const router = express.Router();

// Apply authentication middleware to all client routes
router.use(authenticate);

/**
 * @route GET /api/clients
 * @desc Get all clients with pagination and filtering
 * @access Private
 */
router.get('/', clientController.getClients);

/**
 * @route POST /api/clients
 * @desc Create a new client
 * @access Private
 */
router.post('/', clientController.createClient);

/**
 * @route GET /api/clients/:id
 * @desc Get a client by ID
 * @access Private
 */
router.get('/:id', clientController.getClientById);

/**
 * @route PUT /api/clients/:id
 * @desc Update a client
 * @access Private
 */
router.put('/:id', clientController.updateClient);

/**
 * @route DELETE /api/clients/:id
 * @desc Soft delete a client
 * @access Private
 */
router.delete('/:id', clientController.deleteClient);

/**
 * @route DELETE /api/clients/:id/permanent
 * @desc Permanently delete a client (admin only)
 * @access Admin
 */
router.delete(
  '/:id/permanent',
  authorize(['admin']),
  clientController.permanentDeleteClient
);

export default router;