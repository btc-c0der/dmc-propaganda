import { Document } from 'mongoose';

export interface BaseDocument extends Document {
  createdAt: Date;
  updatedAt: Date;
  isActive: boolean;
}

export interface Pagination {
  page: number;
  limit: number;
  total?: number;
  pages?: number;
}

export interface QueryOptions {
  pagination?: Pagination;
  sort?: Record<string, 1 | -1>;
  filter?: Record<string, any>;
  populate?: string | string[];
}

export interface ResponseResult<T> {
  success: boolean;
  data?: T;
  message?: string;
  error?: any;
  pagination?: Pagination;
}

export interface BaseService<T> {
  create(data: Partial<T>): Promise<T>;
  findById(id: string): Promise<T | null>;
  find(options?: QueryOptions): Promise<T[]>;
  update(id: string, data: Partial<T>): Promise<T | null>;
  delete(id: string): Promise<boolean>;
}