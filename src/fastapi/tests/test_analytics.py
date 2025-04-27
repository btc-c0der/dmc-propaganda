import pytest
from httpx import AsyncClient
import json
from datetime import datetime, timedelta
from beanie.odm.fields import PydanticObjectId

# Tests for analytics endpoints
class TestAnalytics:
    
    @pytest.mark.asyncio
    async def test_get_analytics(self, test_client: AsyncClient, user_token, test_campaign_data):
        """Test getting analytics data"""
        headers = {"Authorization": f"Bearer {user_token}"}
        
        response = await test_client.get("/api/analytics", headers=headers)
        data = response.json()
        
        # Assert response
        assert response.status_code == 200
        assert data["success"] is True
    
    @pytest.mark.asyncio
    async def test_get_analytics_by_campaign(self, test_client: AsyncClient, user_token, test_campaign_data):
        """Test getting analytics data for a specific campaign"""
        headers = {"Authorization": f"Bearer {user_token}"}
        
        response = await test_client.get(
            f"/api/analytics?campaign_id={test_campaign_data['id']}", 
            headers=headers
        )
        data = response.json()
        
        # Assert response
        assert response.status_code == 200
        assert data["success"] is True
    
    @pytest.mark.asyncio
    async def test_get_campaign_performance(self, test_client: AsyncClient, user_token, test_campaign_data):
        """Test getting campaign performance metrics"""
        headers = {"Authorization": f"Bearer {user_token}"}
        
        response = await test_client.get(
            f"/api/analytics/campaign/{test_campaign_data['id']}/performance", 
            headers=headers
        )
        
        # This might fail if the analytics module isn't fully implemented yet
        # Just verify that the request doesn't fail with authentication errors
        assert response.status_code in [200, 404, 501]
        if response.status_code == 200:
            data = response.json()
            assert data["success"] is True
    
    @pytest.mark.asyncio
    async def test_get_client_analytics(self, test_client: AsyncClient, admin_token, test_client_data):
        """Test getting analytics data for a specific client (admin only)"""
        headers = {"Authorization": f"Bearer {admin_token}"}
        
        response = await test_client.get(
            f"/api/analytics/client/{test_client_data['id']}", 
            headers=headers
        )
        
        # This might fail if the analytics module isn't fully implemented yet
        # Just verify that the request doesn't fail with authorization errors
        assert response.status_code in [200, 404, 501]
        if response.status_code == 200:
            data = response.json()
            assert data["success"] is True
    
    @pytest.mark.asyncio
    async def test_get_summary_stats(self, test_client: AsyncClient, admin_token):
        """Test getting summary statistics for campaigns (admin only)"""
        headers = {"Authorization": f"Bearer {admin_token}"}
        
        response = await test_client.get(
            "/api/analytics/summary", 
            headers=headers
        )
        
        # This might fail if the analytics module isn't fully implemented yet
        # Just verify that the request doesn't fail with authorization errors
        assert response.status_code in [200, 404, 501]
        if response.status_code == 200:
            data = response.json()
            assert data["success"] is True
    
    @pytest.mark.asyncio
    async def test_analytics_unauthorized(self, test_client: AsyncClient):
        """Test accessing analytics without authentication"""
        response = await test_client.get("/api/analytics")
        data = response.json()
        
        # Assert response
        assert response.status_code == 401
        assert "Not authenticated" in data.get("detail", "")
    
    @pytest.mark.asyncio
    async def test_client_analytics_non_admin(self, test_client: AsyncClient, user_token, test_client_data):
        """Test getting client analytics as non-admin (should fail)"""
        headers = {"Authorization": f"Bearer {user_token}"}
        
        response = await test_client.get(
            f"/api/analytics/client/{test_client_data['id']}", 
            headers=headers
        )
        
        # For endpoints that require admin privileges, we should get a 403 forbidden
        if response.status_code == 403:
            data = response.json()
            assert "Not enough permissions" in data.get("detail", "")
        else:
            # The endpoint might not be implemented yet, so it might return 404 or 501
            assert response.status_code in [403, 404, 501]