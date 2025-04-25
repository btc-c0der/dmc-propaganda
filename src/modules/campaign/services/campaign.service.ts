import Campaign, { ICampaign } from '../models/campaign.model';
import Client from '../../client/models/client.model';
import { ApiError } from '../../../middleware/errorHandler';
import { QueryOptions } from '../../../interfaces/common';

class CampaignService {
  /**
   * Create a new campaign
   */
  async createCampaign(campaignData: Partial<ICampaign>): Promise<ICampaign> {
    // Verify client exists
    const client = await Client.findById(campaignData.client);
    if (!client) {
      throw new ApiError(400, 'Client not found');
    }

    // Validate dates
    if (campaignData.endDate && campaignData.startDate && 
        new Date(campaignData.endDate) < new Date(campaignData.startDate)) {
      throw new ApiError(400, 'End date must be after start date');
    }

    // Create new campaign
    const campaign = await Campaign.create(campaignData);
    return campaign;
  }

  /**
   * Get all campaigns with optional filtering, pagination, and sorting
   */
  async getCampaigns(options?: QueryOptions): Promise<{
    campaigns: ICampaign[];
    total: number;
    page: number;
    limit: number;
    pages: number;
  }> {
    const page = options?.pagination?.page || 1;
    const limit = options?.pagination?.limit || 10;
    const skip = (page - 1) * limit;
    
    // Build filter query
    const filter = { ...options?.filter, isActive: true };
    
    // Execute query with populate
    const campaigns = await Campaign.find(filter)
      .populate('client', 'name contactPerson')
      .populate('team', 'name email')
      .sort(options?.sort || { startDate: -1 })
      .skip(skip)
      .limit(limit);
    
    // Get total count
    const total = await Campaign.countDocuments(filter);
    
    return {
      campaigns,
      total,
      page,
      limit,
      pages: Math.ceil(total / limit),
    };
  }

  /**
   * Get campaigns by client ID
   */
  async getCampaignsByClientId(clientId: string, options?: QueryOptions): Promise<{
    campaigns: ICampaign[];
    total: number;
    page: number;
    limit: number;
    pages: number;
  }> {
    // Verify client exists
    const client = await Client.findById(clientId);
    if (!client) {
      throw new ApiError(400, 'Client not found');
    }

    const page = options?.pagination?.page || 1;
    const limit = options?.pagination?.limit || 10;
    const skip = (page - 1) * limit;
    
    // Build filter query with client ID
    const filter = { ...options?.filter, client: clientId, isActive: true };
    
    // Execute query
    const campaigns = await Campaign.find(filter)
      .populate('client', 'name contactPerson')
      .populate('team', 'name email')
      .sort(options?.sort || { startDate: -1 })
      .skip(skip)
      .limit(limit);
    
    // Get total count
    const total = await Campaign.countDocuments(filter);
    
    return {
      campaigns,
      total,
      page,
      limit,
      pages: Math.ceil(total / limit),
    };
  }

  /**
   * Get a campaign by ID
   */
  async getCampaignById(id: string): Promise<ICampaign> {
    const campaign = await Campaign.findById(id)
      .populate('client', 'name contactPerson email')
      .populate('team', 'name email')
      .populate('assets');
    
    if (!campaign) {
      throw new ApiError(404, 'Campaign not found');
    }
    
    return campaign;
  }

  /**
   * Update a campaign
   */
  async updateCampaign(id: string, updateData: Partial<ICampaign>): Promise<ICampaign> {
    const campaign = await Campaign.findById(id);
    
    if (!campaign) {
      throw new ApiError(404, 'Campaign not found');
    }
    
    // Validate client if changed
    if (updateData.client && updateData.client.toString() !== campaign.client.toString()) {
      const client = await Client.findById(updateData.client);
      if (!client) {
        throw new ApiError(400, 'Client not found');
      }
    }
    
    // Validate dates
    if ((updateData.endDate || campaign.endDate) && (updateData.startDate || campaign.startDate)) {
      const startDate = updateData.startDate ? new Date(updateData.startDate) : campaign.startDate;
      const endDate = updateData.endDate ? new Date(updateData.endDate) : campaign.endDate;
      
      if (endDate && startDate && endDate < startDate) {
        throw new ApiError(400, 'End date must be after start date');
      }
    }
    
    // Update campaign
    Object.assign(campaign, updateData);
    await campaign.save();
    
    return campaign;
  }

  /**
   * Update campaign status
   */
  async updateCampaignStatus(id: string, status: 'draft' | 'active' | 'completed' | 'cancelled'): Promise<ICampaign> {
    const campaign = await Campaign.findById(id);
    
    if (!campaign) {
      throw new ApiError(404, 'Campaign not found');
    }
    
    campaign.status = status;
    await campaign.save();
    
    return campaign;
  }

  /**
   * Update campaign metrics
   */
  async updateCampaignMetrics(id: string, metrics: ICampaign['metrics']): Promise<ICampaign> {
    const campaign = await Campaign.findById(id);
    
    if (!campaign) {
      throw new ApiError(404, 'Campaign not found');
    }
    
    campaign.metrics = {
      ...campaign.metrics,
      ...metrics,
    };
    
    await campaign.save();
    
    return campaign;
  }

  /**
   * Delete a campaign (soft delete)
   */
  async deleteCampaign(id: string): Promise<boolean> {
    const campaign = await Campaign.findById(id);
    
    if (!campaign) {
      throw new ApiError(404, 'Campaign not found');
    }
    
    campaign.isActive = false;
    await campaign.save();
    
    return true;
  }

  /**
   * Add team members to a campaign
   */
  async addTeamMembers(id: string, teamMemberIds: string[]): Promise<ICampaign> {
    const campaign = await Campaign.findById(id);
    
    if (!campaign) {
      throw new ApiError(404, 'Campaign not found');
    }
    
    // Add team members that aren't already in the team
    const currentTeam = campaign.team?.map(member => member.toString()) || [];
    const newTeamMembers = teamMemberIds.filter(id => !currentTeam.includes(id));
    
    if (newTeamMembers.length > 0) {
      campaign.team = [...(campaign.team || []), ...newTeamMembers.map(id => new mongoose.Types.ObjectId(id))];
      await campaign.save();
    }
    
    return campaign;
  }

  /**
   * Remove team members from a campaign
   */
  async removeTeamMember(id: string, teamMemberId: string): Promise<ICampaign> {
    const campaign = await Campaign.findById(id);
    
    if (!campaign) {
      throw new ApiError(404, 'Campaign not found');
    }
    
    // Filter out the team member
    campaign.team = campaign.team?.filter(
      member => member.toString() !== teamMemberId
    );
    
    await campaign.save();
    
    return campaign;
  }
}

export default new CampaignService();