import express from 'express';
import campaignController from '../controllers/campaign.controller';
import { authenticate, authorize } from '../../../middleware/authMiddleware';

const router = express.Router();

// Apply authentication middleware to all campaign routes
router.use(authenticate);

/**
 * @route GET /api/campaigns
 * @desc Get all campaigns with pagination and filtering
 * @access Private
 */
router.get('/', campaignController.getCampaigns);

/**
 * @route POST /api/campaigns
 * @desc Create a new campaign
 * @access Private
 */
router.post('/', campaignController.createCampaign);

/**
 * @route GET /api/campaigns/client/:clientId
 * @desc Get campaigns by client ID
 * @access Private
 */
router.get('/client/:clientId', campaignController.getCampaignsByClientId);

/**
 * @route GET /api/campaigns/:id
 * @desc Get a campaign by ID
 * @access Private
 */
router.get('/:id', campaignController.getCampaignById);

/**
 * @route PUT /api/campaigns/:id
 * @desc Update a campaign
 * @access Private
 */
router.put('/:id', campaignController.updateCampaign);

/**
 * @route PATCH /api/campaigns/:id/status
 * @desc Update campaign status
 * @access Private
 */
router.patch('/:id/status', campaignController.updateCampaignStatus);

/**
 * @route PATCH /api/campaigns/:id/metrics
 * @desc Update campaign metrics
 * @access Private
 */
router.patch('/:id/metrics', campaignController.updateCampaignMetrics);

/**
 * @route DELETE /api/campaigns/:id
 * @desc Delete a campaign (soft delete)
 * @access Private
 */
router.delete('/:id', campaignController.deleteCampaign);

/**
 * @route POST /api/campaigns/:id/team
 * @desc Add team members to a campaign
 * @access Private (Manager/Admin)
 */
router.post(
  '/:id/team',
  authorize(['admin', 'manager']),
  campaignController.addTeamMembers
);

/**
 * @route DELETE /api/campaigns/:id/team/:memberId
 * @desc Remove a team member from a campaign
 * @access Private (Manager/Admin)
 */
router.delete(
  '/:id/team/:memberId',
  authorize(['admin', 'manager']),
  campaignController.removeTeamMember
);

export default router;