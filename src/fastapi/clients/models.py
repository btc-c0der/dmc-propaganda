from beanie import Document
from pydantic import BaseModel, EmailStr, Field, HttpUrl
from typing import Optional, Dict, List
from datetime import datetime

class SocialMediaHandles(BaseModel):
    """Social media handles model"""
    facebook: Optional[str] = None
    instagram: Optional[str] = None
    twitter: Optional[str] = None
    linkedin: Optional[str] = None
    youtube: Optional[str] = None

class Address(BaseModel):
    """Address model"""
    street: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    postalCode: Optional[str] = None
    country: Optional[str] = None

class Client(Document):
    """Client model for client management"""
    name: str
    contactPerson: str
    email: EmailStr
    phone: str
    address: Optional[Address] = None
    industry: Optional[str] = None
    logo: Optional[str] = None  # URL to logo image
    website: Optional[str] = None
    socialMediaHandles: Optional[SocialMediaHandles] = None
    notes: Optional[str] = None
    isActive: bool = True
    createdAt: datetime = Field(default_factory=datetime.utcnow)
    updatedAt: datetime = Field(default_factory=datetime.utcnow)
    
    class Settings:
        name = "clients"
        
    class Config:
        json_encoders = {
            datetime: lambda dt: dt.isoformat()
        }
        schema_extra = {
            "example": {
                "name": "Example Client",
                "contactPerson": "John Smith",
                "email": "john@exampleclient.com",
                "phone": "+1234567890",
                "industry": "Technology"
            }
        }
        
# Client request/response schemas
class ClientCreate(BaseModel):
    name: str
    contactPerson: str
    email: EmailStr
    phone: str
    address: Optional[Address] = None
    industry: Optional[str] = None
    logo: Optional[str] = None
    website: Optional[str] = None
    socialMediaHandles: Optional[SocialMediaHandles] = None
    notes: Optional[str] = None
    
class ClientUpdate(BaseModel):
    name: Optional[str] = None
    contactPerson: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    address: Optional[Address] = None
    industry: Optional[str] = None
    logo: Optional[str] = None
    website: Optional[str] = None
    socialMediaHandles: Optional[SocialMediaHandles] = None
    notes: Optional[str] = None
    isActive: Optional[bool] = None
    
class ClientResponse(BaseModel):
    id: str
    name: str
    contactPerson: str
    email: EmailStr
    phone: str
    address: Optional[Address] = None
    industry: Optional[str] = None
    logo: Optional[str] = None
    website: Optional[str] = None
    socialMediaHandles: Optional[SocialMediaHandles] = None
    notes: Optional[str] = None
    isActive: bool
    createdAt: datetime
    updatedAt: datetime