import mongoose, { Schema } from 'mongoose';
import { BaseDocument } from '../../../interfaces/common';

export interface ICampaign extends BaseDocument {
  name: string;
  client: mongoose.Types.ObjectId;
  description: string;
  startDate: Date;
  endDate?: Date;
  budget: number;
  status: 'draft' | 'active' | 'completed' | 'cancelled';
  objectives: string[];
  targetAudience?: {
    demographics?: string;
    interests?: string[];
    location?: string;
  };
  channels?: string[];
  metrics?: {
    impressions?: number;
    clicks?: number;
    conversions?: number;
    roi?: number;
  };
  assets?: mongoose.Types.ObjectId[];
  team?: mongoose.Types.ObjectId[];
}

const CampaignSchema: Schema = new Schema(
  {
    name: {
      type: String,
      required: [true, 'Campaign name is required'],
      trim: true,
      maxlength: [100, 'Name cannot be more than 100 characters'],
    },
    client: {
      type: mongoose.Schema.Types.ObjectId,
      ref: 'Client',
      required: [true, 'Client is required'],
    },
    description: {
      type: String,
      required: [true, 'Campaign description is required'],
    },
    startDate: {
      type: Date,
      required: [true, 'Start date is required'],
    },
    endDate: {
      type: Date,
    },
    budget: {
      type: Number,
      required: [true, 'Budget is required'],
    },
    status: {
      type: String,
      enum: ['draft', 'active', 'completed', 'cancelled'],
      default: 'draft',
    },
    objectives: {
      type: [String],
      required: [true, 'Campaign objectives are required'],
    },
    targetAudience: {
      demographics: String,
      interests: [String],
      location: String,
    },
    channels: {
      type: [String],
    },
    metrics: {
      impressions: Number,
      clicks: Number,
      conversions: Number,
      roi: Number,
    },
    assets: [
      {
        type: mongoose.Schema.Types.ObjectId,
        ref: 'Media',
      },
    ],
    team: [
      {
        type: mongoose.Schema.Types.ObjectId,
        ref: 'User',
      },
    ],
    isActive: {
      type: Boolean,
      default: true,
    },
  },
  {
    timestamps: true,
  }
);

export default mongoose.model<ICampaign>('Campaign', CampaignSchema);