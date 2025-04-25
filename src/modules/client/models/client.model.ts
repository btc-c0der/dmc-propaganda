import mongoose, { Schema } from 'mongoose';
import { BaseDocument } from '../../../interfaces/common';

export interface IClient extends BaseDocument {
  name: string;
  contactPerson: string;
  email: string;
  phone: string;
  address?: {
    street: string;
    city: string;
    state: string;
    postalCode: string;
    country: string;
  };
  industry?: string;
  logo?: string;
  website?: string;
  socialMediaHandles?: {
    facebook?: string;
    instagram?: string;
    twitter?: string;
    linkedin?: string;
    youtube?: string;
  };
  notes?: string;
}

const ClientSchema: Schema = new Schema(
  {
    name: {
      type: String,
      required: [true, 'Client name is required'],
      trim: true,
      maxlength: [100, 'Name cannot be more than 100 characters'],
    },
    contactPerson: {
      type: String,
      required: [true, 'Contact person name is required'],
      trim: true,
    },
    email: {
      type: String,
      required: [true, 'Email is required'],
      trim: true,
      lowercase: true,
      match: [
        /^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$/,
        'Please provide a valid email',
      ],
    },
    phone: {
      type: String,
      required: [true, 'Phone number is required'],
      trim: true,
    },
    address: {
      street: String,
      city: String,
      state: String,
      postalCode: String,
      country: String,
    },
    industry: {
      type: String,
      trim: true,
    },
    logo: {
      type: String, // URL to logo image
    },
    website: {
      type: String,
      trim: true,
    },
    socialMediaHandles: {
      facebook: String,
      instagram: String,
      twitter: String,
      linkedin: String,
      youtube: String,
    },
    notes: {
      type: String,
    },
    isActive: {
      type: Boolean,
      default: true,
    },
  },
  {
    timestamps: true,
  }
);

export default mongoose.model<IClient>('Client', ClientSchema);