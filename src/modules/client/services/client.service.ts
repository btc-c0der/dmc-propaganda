import Client, { IClient } from '../models/client.model';
import { ApiError } from '../../../middleware/errorHandler';
import { QueryOptions } from '../../../interfaces/common';

class ClientService {
  /**
   * Create a new client
   */
  async createClient(clientData: Partial<IClient>): Promise<IClient> {
    // Check if client with same name already exists
    const existingClient = await Client.findOne({ name: clientData.name });
    if (existingClient) {
      throw new ApiError(400, 'A client with this name already exists');
    }

    // Create new client
    const client = await Client.create(clientData);
    return client;
  }

  /**
   * Get all clients with optional filtering, pagination, and sorting
   */
  async getClients(options?: QueryOptions): Promise<{
    clients: IClient[];
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
    
    // Execute query
    const clients = await Client.find(filter)
      .sort(options?.sort || { createdAt: -1 })
      .skip(skip)
      .limit(limit);
    
    // Get total count
    const total = await Client.countDocuments(filter);
    
    return {
      clients,
      total,
      page,
      limit,
      pages: Math.ceil(total / limit),
    };
  }

  /**
   * Get a client by ID
   */
  async getClientById(id: string): Promise<IClient> {
    const client = await Client.findById(id);
    
    if (!client) {
      throw new ApiError(404, 'Client not found');
    }
    
    return client;
  }

  /**
   * Update a client
   */
  async updateClient(id: string, updateData: Partial<IClient>): Promise<IClient> {
    const client = await Client.findById(id);
    
    if (!client) {
      throw new ApiError(404, 'Client not found');
    }
    
    // Check if name is being updated and if it's already taken
    if (updateData.name && updateData.name !== client.name) {
      const existingClient = await Client.findOne({ name: updateData.name });
      if (existingClient) {
        throw new ApiError(400, 'A client with this name already exists');
      }
    }
    
    // Update client
    Object.assign(client, updateData);
    await client.save();
    
    return client;
  }

  /**
   * Delete a client (soft delete by setting isActive to false)
   */
  async deleteClient(id: string): Promise<boolean> {
    const client = await Client.findById(id);
    
    if (!client) {
      throw new ApiError(404, 'Client not found');
    }
    
    client.isActive = false;
    await client.save();
    
    return true;
  }

  /**
   * Permanently delete a client (for admin use only)
   */
  async permanentDeleteClient(id: string): Promise<boolean> {
    const result = await Client.findByIdAndDelete(id);
    
    if (!result) {
      throw new ApiError(404, 'Client not found');
    }
    
    return true;
  }
}

export default new ClientService();