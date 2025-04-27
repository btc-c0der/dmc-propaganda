from beanie import Document, Link
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime
from auth.models import User
from clients.models import Client

class TargetAudience(BaseModel):
    """Target audience model for campaigns"""
    demographics: Optional[str] = None
    interests: Optional[List[str]] = None
    location: Optional[str] = None

class CampaignMetrics(BaseModel):
    """Metrics model for campaign performance"""
    impressions: Optional[int] = None
    clicks: Optional[int] = None
    conversions: Optional[int] = None
    roi: Optional[float] = None

class Campaign(Document):
    """Campaign model for campaign management"""
    name: str
    client: Link[Client]
    description: str
    startDate: datetime
    endDate: Optional[datetime] = None
    budget: float
    status: str = "draft"  # draft, active, completed, cancelled
    objectives: List[str] = []
    targetAudience: Optional[TargetAudience] = None
    channels: Optional[List[str]] = None
    metrics: Optional[CampaignMetrics] = None
    assets: Optional[List[str]] = None  # List of asset IDs or URLs
    team: Optional[List[Link[User]]] = None
    isActive: bool = True
    createdAt: datetime = Field(default_factory=datetime.utcnow)
    updatedAt: datetime = Field(default_factory=datetime.utcnow)
    
    class Settings:
        name = "campaigns"
        
    class Config:
        json_encoders = {
            datetime: lambda dt: dt.isoformat()
        }
        schema_extra = {
            "example": {
                "name": "Summer Marketing Campaign",
                "description": "Summer promotion for our products",
                "startDate": "2025-06-01T00:00:00Z",
                "endDate": "2025-08-31T00:00:00Z",
                "budget": 10000,
                "status": "active",
                "objectives": ["Increase brand awareness", "Generate leads"]
            }
        }
        
# Campaign request/response schemas
class CampaignCreate(BaseModel):
    name: str
    client: str  # Client ID
    description: str
    startDate: datetime
    endDate: Optional[datetime] = None
    budget: float
    status: Optional[str] = "draft"
    objectives: Optional[List[str]] = []
    targetAudience: Optional[TargetAudience] = None
    channels: Optional[List[str]] = None
    
class CampaignUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    startDate: Optional[datetime] = None
    endDate: Optional[datetime] = None
    budget: Optional[float] = None
    status: Optional[str] = None
    objectives: Optional[List[str]] = None
    targetAudience: Optional[TargetAudience] = None
    channels: Optional[List[str]] = None
    isActive: Optional[bool] = None
    
class UpdateCampaignStatus(BaseModel):
    status: str
    
class UpdateCampaignMetrics(BaseModel):
    metrics: CampaignMetrics
    
class AddTeamMembers(BaseModel):
    teamMembers: List[str]  # List of user IDs
    
class CampaignResponse(BaseModel):
    id: str
    name: str
    client: Dict[str, Any]  # Client details
    description: str
    startDate: datetime
    endDate: Optional[datetime] = None
    budget: float
    status: str
    objectives: List[str]
    targetAudience: Optional[TargetAudience] = None
    channels: Optional[List[str]] = None
    metrics: Optional[CampaignMetrics] = None
    team: Optional[List[Dict[str, Any]]] = None  # Team member details
    isActive: bool
    createdAt: datetime
    updatedAt: datetime