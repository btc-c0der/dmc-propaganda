import { Request, Response, NextFunction } from 'express';
import campaignService from '../services/campaign.service';
import { ApiResponse } from '../../../utils/responses';
import { QueryOptions } from '../../../interfaces/common';

class CampaignController {
  /**
   * Create a new campaign
   * @route POST /api/campaigns
   */
  async createCampaign(req: Request, res: Response, next: NextFunction) {
    try {
      const campaign = await campaignService.createCampaign(req.body);
      return ApiResponse.success(res, campaign, 'Campaign created successfully', 201);
    } catch (error) {
      next(error);
    }
  }

  /**
   * Get all campaigns with pagination and filtering
   * @route GET /api/campaigns
   */
  async getCampaigns(req: Request, res: Response, next: NextFunction) {
    try {
      // Parse query parameters
      const page = parseInt(req.query.page as string) || 1;
      const limit = parseInt(req.query.limit as string) || 10;
      const sortField = (req.query.sortField as string) || 'startDate';
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

      if (req.query.status) {
        queryOptions.filter = { 
          ...queryOptions.filter, 
          status: req.query.status 
        };
      }

      const result = await campaignService.getCampaigns(queryOptions);
      
      return ApiResponse.success(
        res,
        result.campaigns,
        'Campaigns retrieved successfully',
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
   * Get campaigns by client ID
   * @route GET /api/campaigns/client/:clientId
   */
  async getCampaignsByClientId(req: Request, res: Response, next: NextFunction) {
    try {
      const clientId = req.params.clientId;
      const page = parseInt(req.query.page as string) || 1;
      const limit = parseInt(req.query.limit as string) || 10;
      
      const queryOptions: QueryOptions = {
        pagination: { page, limit },
        sort: { startDate: -1 },
      };
      
      const result = await campaignService.getCampaignsByClientId(clientId, queryOptions);
      
      return ApiResponse.success(
        res,
        result.campaigns,
        'Client campaigns retrieved successfully',
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
   * Get campaign by ID
   * @route GET /api/campaigns/:id
   */
  async getCampaignById(req: Request, res: Response, next: NextFunction) {
    try {
      const campaign = await campaignService.getCampaignById(req.params.id);
      return ApiResponse.success(res, campaign, 'Campaign retrieved successfully');
    } catch (error) {
      next(error);
    }
  }

  /**
   * Update campaign
   * @route PUT /api/campaigns/:id
   */
  async updateCampaign(req: Request, res: Response, next: NextFunction) {
    try {
      const campaign = await campaignService.updateCampaign(req.params.id, req.body);
      return ApiResponse.success(res, campaign, 'Campaign updated successfully');
    } catch (error) {
      next(error);
    }
  }

  /**
   * Update campaign status
   * @route PATCH /api/campaigns/:id/status
   */
  async updateCampaignStatus(req: Request, res: Response, next: NextFunction) {
    try {
      const { status } = req.body;
      
      if (!status || !['draft', 'active', 'completed', 'cancelled'].includes(status)) {
        return ApiResponse.badRequest(res, 'Invalid status provided');
      }
      
      const campaign = await campaignService.updateCampaignStatus(req.params.id, status);
      return ApiResponse.success(res, campaign, `Campaign status updated to ${status}`);
    } catch (error) {
      next(error);
    }
  }

  /**
   * Update campaign metrics
   * @route PATCH /api/campaigns/:id/metrics
   */
  async updateCampaignMetrics(req: Request, res: Response, next: NextFunction) {
    try {
      const { metrics } = req.body;
      
      if (!metrics || typeof metrics !== 'object') {
        return ApiResponse.badRequest(res, 'Valid metrics object is required');
      }
      
      const campaign = await campaignService.updateCampaignMetrics(req.params.id, metrics);
      return ApiResponse.success(res, campaign, 'Campaign metrics updated successfully');
    } catch (error) {
      next(error);
    }
  }

  /**
   * Delete campaign (soft delete)
   * @route DELETE /api/campaigns/:id
   */
  async deleteCampaign(req: Request, res: Response, next: NextFunction) {
    try {
      await campaignService.deleteCampaign(req.params.id);
      return ApiResponse.success(res, null, 'Campaign deleted successfully');
    } catch (error) {
      next(error);
    }
  }

  /**
   * Add team members to a campaign
   * @route POST /api/campaigns/:id/team
   */
  async addTeamMembers(req: Request, res: Response, next: NextFunction) {
    try {
      const { teamMembers } = req.body;
      
      if (!teamMembers || !Array.isArray(teamMembers) || teamMembers.length === 0) {
        return ApiResponse.badRequest(res, 'Valid team members array is required');
      }
      
      const campaign = await campaignService.addTeamMembers(req.params.id, teamMembers);
      return ApiResponse.success(res, campaign, 'Team members added to campaign');
    } catch (error) {
      next(error);
    }
  }

  /**
   * Remove a team member from a campaign
   * @route DELETE /api/campaigns/:id/team/:memberId
   */
  async removeTeamMember(req: Request, res: Response, next: NextFunction) {
    try {
      const campaign = await campaignService.removeTeamMember(req.params.id, req.params.memberId);
      return ApiResponse.success(res, campaign, 'Team member removed from campaign');
    } catch (error) {
      next(error);
    }
  }
}

export default new CampaignController();