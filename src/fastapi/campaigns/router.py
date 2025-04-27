from fastapi import APIRouter, Depends, HTTPException, status, Query
from typing import List, Dict, Any, Optional
from datetime import datetime
from .models import (
    Campaign, CampaignCreate, CampaignUpdate, CampaignResponse, 
    UpdateCampaignStatus, UpdateCampaignMetrics, AddTeamMembers
)
from clients.models import Client
from auth.models import User
from auth.jwt import get_current_user, role_required

router = APIRouter()

@router.post("/", response_model=Dict[str, Any], status_code=status.HTTP_201_CREATED)
async def create_campaign(
    campaign_data: CampaignCreate,
    current_user: User = Depends(get_current_user)
):
    """Create a new campaign"""
    # Verify client exists
    client = await Client.get(campaign_data.client)
    if not client or not client.isActive:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Client not found"
        )
    
    # Validate dates
    if campaign_data.endDate and campaign_data.startDate > campaign_data.endDate:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="End date must be after start date"
        )
    
    # Create new campaign
    new_campaign = Campaign(
        name=campaign_data.name,
        client=client,
        description=campaign_data.description,
        startDate=campaign_data.startDate,
        endDate=campaign_data.endDate,
        budget=campaign_data.budget,
        status=campaign_data.status,
        objectives=campaign_data.objectives,
        targetAudience=campaign_data.targetAudience,
        channels=campaign_data.channels
    )
    
    await new_campaign.create()
    
    # Create response
    response = {
        "success": True,
        "data": {
            "id": str(new_campaign.id),
            "name": new_campaign.name,
            "client": {
                "id": str(client.id),
                "name": client.name
            },
            "startDate": new_campaign.startDate,
            "endDate": new_campaign.endDate,
            "budget": new_campaign.budget,
            "status": new_campaign.status
        },
        "message": "Campaign created successfully"
    }
    
    return response

@router.get("/", response_model=Dict[str, Any])
async def get_campaigns(
    page: int = Query(1, ge=1, description="Page number"),
    limit: int = Query(10, ge=1, le=100, description="Items per page"),
    name: Optional[str] = None,
    status: Optional[str] = None,
    current_user: User = Depends(get_current_user)
):
    """Get all campaigns with filtering and pagination"""
    # Build query filter
    query = {}
    if name:
        query["name"] = {"$regex": name, "$options": "i"}
    if status:
        query["status"] = status
    query["isActive"] = True
    
    # Calculate pagination
    skip = (page - 1) * limit
    
    # Get campaigns with pagination
    campaigns = await Campaign.find(query).skip(skip).limit(limit).sort(-Campaign.startDate).to_list()
    
    # Get total count
    total = await Campaign.count_documents(query)
    
    # Create response with populated client data
    response_data = []
    for campaign in campaigns:
        # Fetch client data
        client = await campaign.client.fetch()
        
        response_data.append({
            "id": str(campaign.id),
            "name": campaign.name,
            "client": {
                "id": str(client.id),
                "name": client.name
            },
            "startDate": campaign.startDate,
            "endDate": campaign.endDate,
            "budget": campaign.budget,
            "status": campaign.status
        })
    
    # Create response
    response = {
        "success": True,
        "data": response_data,
        "message": "Campaigns retrieved successfully",
        "pagination": {
            "page": page,
            "limit": limit,
            "total": total,
            "pages": (total + limit - 1) // limit  # ceiling division
        }
    }
    
    return response

@router.get("/client/{client_id}", response_model=Dict[str, Any])
async def get_campaigns_by_client(
    client_id: str,
    page: int = Query(1, ge=1, description="Page number"),
    limit: int = Query(10, ge=1, le=100, description="Items per page"),
    current_user: User = Depends(get_current_user)
):
    """Get campaigns by client ID"""
    # Verify client exists
    client = await Client.get(client_id)
    if not client or not client.isActive:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Client not found"
        )
    
    # Build query filter
    query = {"client": client, "isActive": True}
    
    # Calculate pagination
    skip = (page - 1) * limit
    
    # Get campaigns with pagination
    campaigns = await Campaign.find(query).skip(skip).limit(limit).sort(-Campaign.startDate).to_list()
    
    # Get total count
    total = await Campaign.count_documents(query)
    
    # Create response data
    response_data = []
    for campaign in campaigns:
        response_data.append({
            "id": str(campaign.id),
            "name": campaign.name,
            "startDate": campaign.startDate,
            "endDate": campaign.endDate,
            "budget": campaign.budget,
            "status": campaign.status
        })
    
    # Create response
    response = {
        "success": True,
        "data": response_data,
        "message": "Client campaigns retrieved successfully",
        "pagination": {
            "page": page,
            "limit": limit,
            "total": total,
            "pages": (total + limit - 1) // limit  # ceiling division
        }
    }
    
    return response

@router.get("/{campaign_id}", response_model=Dict[str, Any])
async def get_campaign_by_id(
    campaign_id: str,
    current_user: User = Depends(get_current_user)
):
    """Get a campaign by ID"""
    campaign = await Campaign.get(campaign_id)
    if not campaign or not campaign.isActive:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Campaign not found"
        )
    
    # Fetch client data
    client = await campaign.client.fetch()
    
    # Fetch team members if present
    team_data = []
    if campaign.team:
        for team_member_link in campaign.team:
            try:
                team_member = await team_member_link.fetch()
                team_data.append({
                    "id": str(team_member.id),
                    "name": team_member.name,
                    "email": team_member.email
                })
            except:
                # Handle case where team member might have been deleted
                continue
    
    # Create response
    response = {
        "success": True,
        "data": {
            "id": str(campaign.id),
            "name": campaign.name,
            "client": {
                "id": str(client.id),
                "name": client.name,
                "contactPerson": client.contactPerson,
                "email": client.email
            },
            "description": campaign.description,
            "startDate": campaign.startDate,
            "endDate": campaign.endDate,
            "budget": campaign.budget,
            "status": campaign.status,
            "objectives": campaign.objectives,
            "targetAudience": campaign.targetAudience,
            "channels": campaign.channels,
            "metrics": campaign.metrics,
            "team": team_data,
            "createdAt": campaign.createdAt,
            "updatedAt": campaign.updatedAt
        },
        "message": "Campaign retrieved successfully"
    }
    
    return response

@router.put("/{campaign_id}", response_model=Dict[str, Any])
async def update_campaign(
    campaign_id: str,
    campaign_data: CampaignUpdate,
    current_user: User = Depends(get_current_user)
):
    """Update a campaign"""
    campaign = await Campaign.get(campaign_id)
    if not campaign or not campaign.isActive:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Campaign not found"
        )
    
    # Validate dates if both are provided
    start_date = campaign_data.startDate if campaign_data.startDate else campaign.startDate
    end_date = campaign_data.endDate if campaign_data.endDate else campaign.endDate
    
    if end_date and start_date and end_date < start_date:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="End date must be after start date"
        )
    
    # Update campaign
    update_data = campaign_data.dict(exclude_unset=True)
    update_data["updatedAt"] = datetime.utcnow()
    
    for field, value in update_data.items():
        setattr(campaign, field, value)
    
    await campaign.save()
    
    # Create response
    response = {
        "success": True,
        "data": {
            "id": str(campaign.id),
            "name": campaign.name,
            "status": campaign.status,
            "updatedAt": campaign.updatedAt
        },
        "message": "Campaign updated successfully"
    }
    
    return response

@router.patch("/{campaign_id}/status", response_model=Dict[str, Any])
async def update_campaign_status(
    campaign_id: str,
    status_data: UpdateCampaignStatus,
    current_user: User = Depends(get_current_user)
):
    """Update campaign status"""
    campaign = await Campaign.get(campaign_id)
    if not campaign or not campaign.isActive:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Campaign not found"
        )
    
    # Validate status value
    valid_statuses = ["draft", "active", "completed", "cancelled"]
    if status_data.status not in valid_statuses:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid status. Must be one of {valid_statuses}"
        )
    
    # Update status
    campaign.status = status_data.status
    campaign.updatedAt = datetime.utcnow()
    await campaign.save()
    
    # Create response
    response = {
        "success": True,
        "data": {
            "id": str(campaign.id),
            "name": campaign.name,
            "status": campaign.status
        },
        "message": f"Campaign status updated to {status_data.status}"
    }
    
    return response

@router.patch("/{campaign_id}/metrics", response_model=Dict[str, Any])
async def update_campaign_metrics(
    campaign_id: str,
    metrics_data: UpdateCampaignMetrics,
    current_user: User = Depends(get_current_user)
):
    """Update campaign metrics"""
    campaign = await Campaign.get(campaign_id)
    if not campaign or not campaign.isActive:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Campaign not found"
        )
    
    # Update metrics
    campaign.metrics = metrics_data.metrics
    campaign.updatedAt = datetime.utcnow()
    await campaign.save()
    
    # Create response
    response = {
        "success": True,
        "data": {
            "id": str(campaign.id),
            "name": campaign.name,
            "metrics": campaign.metrics
        },
        "message": "Campaign metrics updated successfully"
    }
    
    return response

@router.post("/{campaign_id}/team", response_model=Dict[str, Any])
async def add_team_members(
    campaign_id: str,
    team_data: AddTeamMembers,
    current_user: User = Depends(role_required(["admin", "manager"]))
):
    """Add team members to a campaign"""
    campaign = await Campaign.get(campaign_id)
    if not campaign or not campaign.isActive:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Campaign not found"
        )
    
    # Initialize team list if None
    if not campaign.team:
        campaign.team = []
    
    # Get current team member IDs for comparison
    current_team_ids = [str(member_link.ref.id) for member_link in campaign.team]
    
    # Add new team members
    team_members_added = []
    for member_id in team_data.teamMembers:
        if member_id not in current_team_ids:
            try:
                team_member = await User.get(member_id)
                if team_member and team_member.isActive:
                    campaign.team.append(team_member)
                    team_members_added.append({
                        "id": str(team_member.id),
                        "name": team_member.name,
                        "email": team_member.email
                    })
            except Exception as e:
                # Skip invalid user IDs
                continue
    
    campaign.updatedAt = datetime.utcnow()
    await campaign.save()
    
    # Create response
    response = {
        "success": True,
        "data": {
            "id": str(campaign.id),
            "name": campaign.name,
            "teamMembersAdded": team_members_added
        },
        "message": "Team members added to campaign"
    }
    
    return response

@router.delete("/{campaign_id}/team/{member_id}", response_model=Dict[str, Any])
async def remove_team_member(
    campaign_id: str,
    member_id: str,
    current_user: User = Depends(role_required(["admin", "manager"]))
):
    """Remove a team member from a campaign"""
    campaign = await Campaign.get(campaign_id)
    if not campaign or not campaign.isActive:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Campaign not found"
        )
    
    # Check if team exists
    if not campaign.team:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Team member not found in campaign"
        )
    
    # Filter out the team member
    campaign.team = [
        member for member in campaign.team 
        if str(member.ref.id) != member_id
    ]
    
    campaign.updatedAt = datetime.utcnow()
    await campaign.save()
    
    # Create response
    response = {
        "success": True,
        "data": None,
        "message": "Team member removed from campaign"
    }
    
    return response

@router.delete("/{campaign_id}", response_model=Dict[str, Any])
async def delete_campaign(
    campaign_id: str,
    current_user: User = Depends(get_current_user)
):
    """Soft delete a campaign"""
    campaign = await Campaign.get(campaign_id)
    if not campaign or not campaign.isActive:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Campaign not found"
        )
    
    # Soft delete (set isActive to False)
    campaign.isActive = False
    campaign.updatedAt = datetime.utcnow()
    await campaign.save()
    
    # Create response
    response = {
        "success": True,
        "data": None,
        "message": "Campaign deleted successfully"
    }
    
    return response