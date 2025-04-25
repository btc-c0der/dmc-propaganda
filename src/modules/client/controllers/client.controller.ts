import { Request, Response, NextFunction } from 'express';
import clientService from '../services/client.service';
import { ApiResponse } from '../../../utils/responses';
import { QueryOptions } from '../../../interfaces/common';

class ClientController {
  /**
   * Create a new client
   * @route POST /api/clients
   */
  async createClient(req: Request, res: Response, next: NextFunction) {
    try {
      const client = await clientService.createClient(req.body);
      return ApiResponse.success(res, client, 'Client created successfully', 201);
    } catch (error) {
      next(error);
    }
  }

  /**
   * Get all clients with pagination
   * @route GET /api/clients
   */
  async getClients(req: Request, res: Response, next: NextFunction) {
    try {
      // Parse query parameters
      const page = parseInt(req.query.page as string) || 1;
      const limit = parseInt(req.query.limit as string) || 10;
      const sortField = (req.query.sortField as string) || 'createdAt';
      const sortOrder = req.query.sortOrder === 'asc' ? 1 : -1;
      
      // Build query options
      const queryOptions: QueryOptions = {
        pagination: { page, limit },
        sort: { [sortField]: sortOrder },
        filter: {},
      };

      // Add filters if provided
      if (req.query.name) {
        queryOptions.filter = { 
          ...queryOptions.filter, 
          name: { $regex: req.query.name, $options: 'i' } 
        };
      }

      if (req.query.industry) {
        queryOptions.filter = { 
          ...queryOptions.filter, 
          industry: req.query.industry 
        };
      }

      const result = await clientService.getClients(queryOptions);
      
      return ApiResponse.success(
        res,
        result.clients,
        'Clients retrieved successfully',
        200,
        {
          page: result.page,
          limit: result.limit,
          total: result.total,
          pages: result.pages,
        }
      );
    } catch (error) {
      next(error);
    }
  }

  /**
   * Get client by ID
   * @route GET /api/clients/:id
   */
  async getClientById(req: Request, res: Response, next: NextFunction) {
    try {
      const client = await clientService.getClientById(req.params.id);
      return ApiResponse.success(res, client, 'Client retrieved successfully');
    } catch (error) {
      next(error);
    }
  }

  /**
   * Update client
   * @route PUT /api/clients/:id
   */
  async updateClient(req: Request, res: Response, next: NextFunction) {
    try {
      const client = await clientService.updateClient(req.params.id, req.body);
      return ApiResponse.success(res, client, 'Client updated successfully');
    } catch (error) {
      next(error);
    }
  }

  /**
   * Delete client (soft delete)
   * @route DELETE /api/clients/:id
   */
  async deleteClient(req: Request, res: Response, next: NextFunction) {
    try {
      await clientService.deleteClient(req.params.id);
      return ApiResponse.success(res, null, 'Client deleted successfully');
    } catch (error) {
      next(error);
    }
  }

  /**
   * Permanently delete client (admin only)
   * @route DELETE /api/clients/:id/permanent
   */
  async permanentDeleteClient(req: Request, res: Response, next: NextFunction) {
    try {
      await clientService.permanentDeleteClient(req.params.id);
      return ApiResponse.success(res, null, 'Client permanently deleted');
    } catch (error) {
      next(error);
    }
  }
}

export default new ClientController();