from fastapi import APIRouter, Depends, HTTPException, status, Query
from typing import Dict, Any, Optional, List
from datetime import datetime, timedelta
from auth.jwt import get_current_user, role_required
from auth.models import User
from campaigns.models import Campaign
from clients.models import Client

router = APIRouter()

@router.get("/", response_model=Dict[str, Any])
async def get_analytics(
    campaign_id: Optional[str] = None,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    current_user: User = Depends(get_current_user)
):
    """Get analytics data with optional campaign filtering"""
    response = {
        "success": True,
        "data": {
            "summary": {
                "totalCampaigns": await Campaign.find({"isActive": True}).count(),
                "totalClients": await Client.find({"isActive": True}).count(),
                "dateGenerated": datetime.utcnow()
            }
        },
        "message": "Analytics retrieved successfully"
    }
    
    # If campaign_id is provided, get campaign-specific analytics
    if campaign_id:
        campaign = await Campaign.get(campaign_id)
        if not campaign or not campaign.isActive:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Campaign not found"
            )
        
        # Add campaign metrics to response if available
        campaign_data = {
            "id": str(campaign.id),
            "name": campaign.name,
            "metrics": campaign.metrics if campaign.metrics else {
                "impressions": 0,
                "clicks": 0,
                "conversions": 0,
                "roi": 0.0
            }
        }
        
        response["data"]["campaign"] = campaign_data
    
    return response

@router.get("/campaign/{campaign_id}/performance", response_model=Dict[str, Any])
async def get_campaign_performance(
    campaign_id: str,
    current_user: User = Depends(get_current_user)
):
    """Get detailed performance metrics for a campaign"""
    campaign = await Campaign.get(campaign_id)
    if not campaign or not campaign.isActive:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Campaign not found"
        )
    
    # Get client info
    client = await campaign.client.fetch()
    
    # Sample performance data - in a real implementation this would come from a database or analytics service
    performance_data = {
        "dailyMetrics": [
            {
                "date": (datetime.utcnow() - timedelta(days=d)).strftime("%Y-%m-%d"),
                "impressions": 100 * (30 - d),
                "clicks": 10 * (30 - d),
                "conversions": max(1, (30 - d) // 3),
                "roi": round(0.5 + (d / 30), 2)
            }
            for d in range(30)
        ],
        "channelPerformance": {
            "social": {"impressions": 15000, "clicks": 1200, "conversions": 120},
            "email": {"impressions": 5000, "clicks": 750, "conversions": 80},
            "web": {"impressions": 8000, "clicks": 900, "conversions": 90}
        }
    }
    
    response = {
        "success": True,
        "data": {
            "campaign": {
                "id": str(campaign.id),
                "name": campaign.name,
                "client": {
                    "id": str(client.id),
                    "name": client.name
                },
                "startDate": campaign.startDate,
                "endDate": campaign.endDate,
                "metrics": campaign.metrics
            },
            "performance": performance_data
        },
        "message": "Campaign performance retrieved successfully"
    }
    
    return response

@router.get("/client/{client_id}", response_model=Dict[str, Any])
async def get_client_analytics(
    client_id: str,
    current_user: User = Depends(role_required(["admin", "manager"]))
):
    """Get analytics data for a specific client (admin/manager only)"""
    client = await Client.get(client_id)
    if not client or not client.isActive:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Client not found"
        )
    
    # Get all active campaigns for this client
    campaigns = await Campaign.find({"client": client, "isActive": True}).to_list()
    
    # Calculate aggregate metrics
    total_impressions = 0
    total_clicks = 0
    total_conversions = 0
    total_budget = 0
    
    campaign_metrics = []
    for campaign in campaigns:
        metrics = campaign.metrics
        budget = campaign.budget
        total_budget += budget
        
        if metrics:
            total_impressions += metrics.impressions or 0
            total_clicks += metrics.clicks or 0
            total_conversions += metrics.conversions or 0
            
            campaign_metrics.append({
                "id": str(campaign.id),
                "name": campaign.name,
                "status": campaign.status,
                "metrics": {
                    "impressions": metrics.impressions or 0,
                    "clicks": metrics.clicks or 0,
                    "conversions": metrics.conversions or 0,
                    "roi": metrics.roi or 0.0
                }
            })
    
    response = {
        "success": True,
        "data": {
            "client": {
                "id": str(client.id),
                "name": client.name
            },
            "summary": {
                "totalCampaigns": len(campaigns),
                "totalBudget": total_budget,
                "totalImpressions": total_impressions,
                "totalClicks": total_clicks,
                "totalConversions": total_conversions,
                "averageCTR": round((total_clicks / total_impressions * 100), 2) if total_impressions > 0 else 0,
                "averageConversionRate": round((total_conversions / total_clicks * 100), 2) if total_clicks > 0 else 0
            },
            "campaigns": campaign_metrics
        },
        "message": "Client analytics retrieved successfully"
    }
    
    return response

@router.get("/summary", response_model=Dict[str, Any])
async def get_summary_stats(
    current_user: User = Depends(role_required(["admin"]))
):
    """Get summary statistics across all campaigns (admin only)"""
    # Get counts
    total_campaigns = await Campaign.count_documents({"isActive": True})
    total_clients = await Client.count_documents({"isActive": True})
    
    # Get active campaigns
    active_campaigns = await Campaign.find({"status": "active", "isActive": True}).count()
    
    # Get campaigns by status
    campaigns_by_status = {
        "draft": await Campaign.count_documents({"status": "draft", "isActive": True}),
        "active": active_campaigns,
        "completed": await Campaign.count_documents({"status": "completed", "isActive": True}),
        "cancelled": await Campaign.count_documents({"status": "cancelled", "isActive": True})
    }
    
    # Calculate today's date and dates for last 30 days
    today = datetime.utcnow().date()
    thirty_days_ago = (today - timedelta(days=30))
    
    # Get campaigns created in the last 30 days
    recent_campaigns = await Campaign.count_documents({
        "createdAt": {"$gte": thirty_days_ago},
        "isActive": True
    })
    
    response = {
        "success": True,
        "data": {
            "counts": {
                "totalCampaigns": total_campaigns,
                "totalClients": total_clients,
                "activeCampaigns": active_campaigns,
                "recentCampaigns": recent_campaigns
            },
            "campaignsByStatus": campaigns_by_status,
            "generatedAt": datetime.utcnow()
        },
        "message": "Summary statistics retrieved successfully"
    }
    
    return response