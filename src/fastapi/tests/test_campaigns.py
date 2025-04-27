import pytest
from httpx import AsyncClient
import json
from datetime import datetime, timedelta

# Tests for campaign endpoints
class TestCampaigns:
    
    @pytest.mark.asyncio
    async def test_create_campaign_success(self, test_client: AsyncClient, user_token, test_client_data, clear_test_data):
        """Test successful campaign creation"""
        # Get current datetime and a future date for campaign duration
        now = datetime.utcnow()
        end_date = now + timedelta(days=90)
        
        # Format dates as strings in ISO format
        start_date_str = now.isoformat()
        end_date_str = end_date.isoformat()
        
        campaign_data = {
            "name": "New Marketing Campaign",
            "client": test_client_data["id"],
            "description": "A new marketing campaign for testing",
            "startDate": start_date_str,
            "endDate": end_date_str,
            "budget": 15000.0,
            "status": "draft",
            "objectives": ["Brand awareness", "Lead generation"],
            "targetAudience": {
                "demographics": "18-35 years, urban",
                "interests": ["social media", "technology"],
                "location": "North America"
            },
            "channels": ["social media", "email marketing"]
        }
        
        headers = {"Authorization": f"Bearer {user_token}"}
        
        response = await test_client.post("/api/campaigns", json=campaign_data, headers=headers)
        data = response.json()
        
        # Assert response
        assert response.status_code == 201
        assert data["success"] is True
        assert data["message"] == "Campaign created successfully"
        assert data["data"]["name"] == campaign_data["name"]
        assert "id" in data["data"]
        assert data["data"]["client"]["id"] == test_client_data["id"]
    
    @pytest.mark.asyncio
    async def test_create_campaign_invalid_client(self, test_client: AsyncClient, user_token):
        """Test campaign creation with an invalid client ID"""
        now = datetime.utcnow()
        end_date = now + timedelta(days=90)
        
        campaign_data = {
            "name": "Invalid Client Campaign",
            "client": "invalidclientid",
            "description": "This campaign should fail validation",
            "startDate": now.isoformat(),
            "endDate": end_date.isoformat(),
            "budget": 10000.0,
            "status": "draft"
        }
        
        headers = {"Authorization": f"Bearer {user_token}"}
        
        response = await test_client.post("/api/campaigns", json=campaign_data, headers=headers)
        data = response.json()
        
        # Assert response
        assert response.status_code == 404
        assert "Client not found" in data.get("detail", "")
    
    @pytest.mark.asyncio
    async def test_create_campaign_invalid_dates(self, test_client: AsyncClient, user_token, test_client_data):
        """Test campaign creation with end date before start date"""
        now = datetime.utcnow()
        # Set end date before start date
        end_date = now - timedelta(days=30)
        
        campaign_data = {
            "name": "Invalid Dates Campaign",
            "client": test_client_data["id"],
            "description": "This campaign should fail date validation",
            "startDate": now.isoformat(),
            "endDate": end_date.isoformat(),  # End date before start date
            "budget": 10000.0
        }
        
        headers = {"Authorization": f"Bearer {user_token}"}
        
        response = await test_client.post("/api/campaigns", json=campaign_data, headers=headers)
        data = response.json()
        
        # Assert response
        assert response.status_code == 400
        assert "End date must be after start date" in data.get("detail", "")
    
    @pytest.mark.asyncio
    async def test_get_campaigns(self, test_client: AsyncClient, user_token, test_campaign_data):
        """Test getting all campaigns"""
        headers = {"Authorization": f"Bearer {user_token}"}
        
        response = await test_client.get("/api/campaigns", headers=headers)
        data = response.json()
        
        # Assert response
        assert response.status_code == 200
        assert data["success"] is True
        assert data["message"] == "Campaigns retrieved successfully"
        assert len(data["data"]) >= 1
        assert "pagination" in data
        
        # Check if our test campaign is in the results
        campaign_found = False
        for campaign in data["data"]:
            if campaign["id"] == test_campaign_data["id"]:
                campaign_found = True
                break
        
        assert campaign_found, "Test campaign not found in the results"
    
    @pytest.mark.asyncio
    async def test_get_campaigns_with_filters(self, test_client: AsyncClient, user_token, test_campaign_data):
        """Test getting campaigns with filters (name, status)"""
        headers = {"Authorization": f"Bearer {user_token}"}
        
        # Test filtering by name
        response = await test_client.get(
            f"/api/campaigns?name={test_campaign_data['name']}", 
            headers=headers
        )
        data = response.json()
        
        assert response.status_code == 200
        assert data["success"] is True
        assert len(data["data"]) >= 1
        assert data["data"][0]["name"] == test_campaign_data["name"]
        
        # Test filtering by status (active)
        response = await test_client.get(
            "/api/campaigns?status=active", 
            headers=headers
        )
        data = response.json()
        
        assert response.status_code == 200
        assert data["success"] is True
        # Check if campaigns have "active" status
        for campaign in data["data"]:
            assert campaign["status"] == "active"
    
    @pytest.mark.asyncio
    async def test_get_campaigns_by_client(self, test_client: AsyncClient, user_token, test_campaign_data, test_client_data):
        """Test getting campaigns by client ID"""
        headers = {"Authorization": f"Bearer {user_token}"}
        
        response = await test_client.get(
            f"/api/campaigns/client/{test_client_data['id']}", 
            headers=headers
        )
        data = response.json()
        
        # Assert response
        assert response.status_code == 200
        assert data["success"] is True
        assert data["message"] == "Client campaigns retrieved successfully"
        assert len(data["data"]) >= 1
        assert "pagination" in data
        
        # Check if our test campaign is in the results
        campaign_found = False
        for campaign in data["data"]:
            if campaign["id"] == test_campaign_data["id"]:
                campaign_found = True
                break
        
        assert campaign_found, "Test campaign not found in client campaigns"
    
    @pytest.mark.asyncio
    async def test_get_campaign_by_id(self, test_client: AsyncClient, user_token, test_campaign_data):
        """Test getting a campaign by ID"""
        headers = {"Authorization": f"Bearer {user_token}"}
        
        response = await test_client.get(
            f"/api/campaigns/{test_campaign_data['id']}", 
            headers=headers
        )
        data = response.json()
        
        # Assert response
        assert response.status_code == 200
        assert data["success"] is True
        assert data["message"] == "Campaign retrieved successfully"
        assert data["data"]["id"] == test_campaign_data["id"]
        assert data["data"]["name"] == test_campaign_data["name"]
        assert "client" in data["data"]
        assert data["data"]["client"]["id"] == test_campaign_data["client_id"]
    
    @pytest.mark.asyncio
    async def test_get_campaign_invalid_id(self, test_client: AsyncClient, user_token):
        """Test getting a campaign with an invalid ID"""
        headers = {"Authorization": f"Bearer {user_token}"}
        
        response = await test_client.get("/api/campaigns/invalidid", headers=headers)
        data = response.json()
        
        # Assert response
        assert response.status_code == 404
        assert "detail" in data
    
    @pytest.mark.asyncio
    async def test_update_campaign(self, test_client: AsyncClient, user_token, test_campaign_data):
        """Test updating a campaign"""
        headers = {"Authorization": f"Bearer {user_token}"}
        
        update_data = {
            "description": "Updated campaign description",
            "budget": 20000.0
        }
        
        response = await test_client.put(
            f"/api/campaigns/{test_campaign_data['id']}", 
            json=update_data,
            headers=headers
        )
        data = response.json()
        
        # Assert response
        assert response.status_code == 200
        assert data["success"] is True
        assert data["message"] == "Campaign updated successfully"
        
        # Verify the update with a GET request
        response = await test_client.get(
            f"/api/campaigns/{test_campaign_data['id']}", 
            headers=headers
        )
        data = response.json()
        
        assert data["data"]["description"] == update_data["description"]
        assert data["data"]["budget"] == update_data["budget"]
    
    @pytest.mark.asyncio
    async def test_update_campaign_status(self, test_client: AsyncClient, user_token, test_campaign_data):
        """Test updating campaign status"""
        headers = {"Authorization": f"Bearer {user_token}"}
        
        status_update = {
            "status": "completed"
        }
        
        response = await test_client.patch(
            f"/api/campaigns/{test_campaign_data['id']}/status", 
            json=status_update,
            headers=headers
        )
        data = response.json()
        
        # Assert response
        assert response.status_code == 200
        assert data["success"] is True
        assert "Campaign status updated" in data["message"]
        assert data["data"]["status"] == status_update["status"]
        
        # Verify the update with a GET request
        response = await test_client.get(
            f"/api/campaigns/{test_campaign_data['id']}", 
            headers=headers
        )
        data = response.json()
        
        assert data["data"]["status"] == status_update["status"]
    
    @pytest.mark.asyncio
    async def test_update_campaign_status_invalid(self, test_client: AsyncClient, user_token, test_campaign_data):
        """Test updating campaign status with an invalid value"""
        headers = {"Authorization": f"Bearer {user_token}"}
        
        status_update = {
            "status": "invalid-status"
        }
        
        response = await test_client.patch(
            f"/api/campaigns/{test_campaign_data['id']}/status", 
            json=status_update,
            headers=headers
        )
        data = response.json()
        
        # Assert response
        assert response.status_code == 400
        assert "Invalid status" in data.get("detail", "")
    
    @pytest.mark.asyncio
    async def test_update_campaign_metrics(self, test_client: AsyncClient, user_token, test_campaign_data):
        """Test updating campaign metrics"""
        headers = {"Authorization": f"Bearer {user_token}"}
        
        metrics_update = {
            "metrics": {
                "impressions": 10000,
                "clicks": 1000,
                "conversions": 100,
                "roi": 3.5
            }
        }
        
        response = await test_client.patch(
            f"/api/campaigns/{test_campaign_data['id']}/metrics", 
            json=metrics_update,
            headers=headers
        )
        data = response.json()
        
        # Assert response
        assert response.status_code == 200
        assert data["success"] is True
        assert data["message"] == "Campaign metrics updated successfully"
        assert data["data"]["metrics"]["impressions"] == metrics_update["metrics"]["impressions"]
        assert data["data"]["metrics"]["clicks"] == metrics_update["metrics"]["clicks"]
        assert data["data"]["metrics"]["conversions"] == metrics_update["metrics"]["conversions"]
        assert data["data"]["metrics"]["roi"] == metrics_update["metrics"]["roi"]
        
        # Verify the update with a GET request
        response = await test_client.get(
            f"/api/campaigns/{test_campaign_data['id']}", 
            headers=headers
        )
        data = response.json()
        
        assert data["data"]["metrics"]["impressions"] == metrics_update["metrics"]["impressions"]
    
    @pytest.mark.asyncio
    async def test_add_team_members(self, test_client: AsyncClient, admin_token, test_campaign_data, test_user):
        """Test adding team members to a campaign as an admin"""
        headers = {"Authorization": f"Bearer {admin_token}"}
        
        team_data = {
            "teamMembers": [test_user["id"]]
        }
        
        response = await test_client.post(
            f"/api/campaigns/{test_campaign_data['id']}/team", 
            json=team_data,
            headers=headers
        )
        data = response.json()
        
        # Assert response
        assert response.status_code == 200
        assert data["success"] is True
        assert data["message"] == "Team members added to campaign"
        assert len(data["data"]["teamMembersAdded"]) == 1
        assert data["data"]["teamMembersAdded"][0]["id"] == test_user["id"]
        
        # Verify the update with a GET request
        response = await test_client.get(
            f"/api/campaigns/{test_campaign_data['id']}", 
            headers=headers
        )
        data = response.json()
        
        # Check if team member was added
        team_member_found = False
        for member in data["data"]["team"]:
            if member["id"] == test_user["id"]:
                team_member_found = True
                break
        
        assert team_member_found, "Team member not found after adding"
    
    @pytest.mark.asyncio
    async def test_add_team_members_non_admin(self, test_client: AsyncClient, user_token, test_campaign_data, test_admin):
        """Test adding team members to a campaign as a non-admin (should fail)"""
        headers = {"Authorization": f"Bearer {user_token}"}
        
        team_data = {
            "teamMembers": [test_admin["id"]]
        }
        
        response = await test_client.post(
            f"/api/campaigns/{test_campaign_data['id']}/team", 
            json=team_data,
            headers=headers
        )
        data = response.json()
        
        # Assert response - should be forbidden for non-admin
        assert response.status_code == 403
        assert "Not enough permissions" in data.get("detail", "")
    
    @pytest.mark.asyncio
    async def test_delete_campaign(self, test_client: AsyncClient, user_token, test_client_data):
        """Test soft deleting a campaign"""
        # Create a new campaign to delete
        now = datetime.utcnow()
        end_date = now + timedelta(days=30)
        
        # Create campaign
        campaign_data = {
            "name": "Campaign To Delete",
            "client": test_client_data["id"],
            "description": "This campaign will be deleted",
            "startDate": now.isoformat(),
            "endDate": end_date.isoformat(),
            "budget": 5000.0,
            "status": "draft"
        }
        
        headers = {"Authorization": f"Bearer {user_token}"}
        
        # Create campaign
        create_response = await test_client.post("/api/campaigns", json=campaign_data, headers=headers)
        create_data = create_response.json()
        campaign_id = create_data["data"]["id"]
        
        # Delete the campaign
        delete_response = await test_client.delete(f"/api/campaigns/{campaign_id}", headers=headers)
        delete_data = delete_response.json()
        
        # Assert delete response
        assert delete_response.status_code == 200
        assert delete_data["success"] is True
        assert delete_data["message"] == "Campaign deleted successfully"
        
        # Try to get the deleted campaign - it should be soft deleted
        get_response = await test_client.get(f"/api/campaigns/{campaign_id}", headers=headers)
        
        assert get_response.status_code == 404