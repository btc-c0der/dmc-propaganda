import pytest
from httpx import AsyncClient
import json
from datetime import datetime

# Tests for client endpoints
class TestClients:
    
    @pytest.mark.asyncio
    async def test_create_client_success(self, test_client: AsyncClient, user_token, clear_test_data):
        """Test successful client creation"""
        client_data = {
            "name": "New Test Client",
            "contactPerson": "Jane Contact",
            "email": "contact@newtestclient.com",
            "phone": "+9876543210",
            "industry": "Healthcare",
            "website": "https://newtestclient.com",
            "address": {
                "street": "456 New St",
                "city": "New City",
                "state": "New State",
                "postalCode": "54321",
                "country": "New Country"
            }
        }
        
        headers = {"Authorization": f"Bearer {user_token}"}
        
        response = await test_client.post("/api/clients", json=client_data, headers=headers)
        data = response.json()
        
        # Assert response
        assert response.status_code == 201
        assert data["success"] is True
        assert data["message"] == "Client created successfully"
        assert data["data"]["name"] == client_data["name"]
        assert data["data"]["email"] == client_data["email"]
        assert "id" in data["data"]
    
    @pytest.mark.asyncio
    async def test_create_client_duplicate_name(self, test_client: AsyncClient, user_token, test_client_data):
        """Test client creation with duplicate name"""
        client_data = {
            "name": test_client_data["name"],  # Using the same name as existing client
            "contactPerson": "Jane Contact",
            "email": "contact@duplicateclient.com",
            "phone": "+9876543210"
        }
        
        headers = {"Authorization": f"Bearer {user_token}"}
        
        response = await test_client.post("/api/clients", json=client_data, headers=headers)
        data = response.json()
        
        # Assert response
        assert response.status_code == 400
        assert "A client with this name already exists" in data.get("detail", "")
    
    @pytest.mark.asyncio
    async def test_create_client_no_auth(self, test_client: AsyncClient):
        """Test client creation without authentication"""
        client_data = {
            "name": "Unauthenticated Client",
            "contactPerson": "No Auth",
            "email": "noauth@example.com",
            "phone": "+1122334455"
        }
        
        response = await test_client.post("/api/clients", json=client_data)
        data = response.json()
        
        # Assert response
        assert response.status_code == 401
        assert "Not authenticated" in data.get("detail", "")
    
    @pytest.mark.asyncio
    async def test_get_clients(self, test_client: AsyncClient, user_token, test_client_data):
        """Test getting all clients"""
        headers = {"Authorization": f"Bearer {user_token}"}
        
        response = await test_client.get("/api/clients", headers=headers)
        data = response.json()
        
        # Assert response
        assert response.status_code == 200
        assert data["success"] is True
        assert data["message"] == "Clients retrieved successfully"
        assert len(data["data"]) >= 1
        assert "pagination" in data
        
        # Check if our test client is in the results
        client_found = False
        for client in data["data"]:
            if client["id"] == test_client_data["id"]:
                client_found = True
                break
        
        assert client_found, "Test client not found in the results"
    
    @pytest.mark.asyncio
    async def test_get_clients_with_filters(self, test_client: AsyncClient, user_token, test_client_data):
        """Test getting clients with filters (name, industry)"""
        headers = {"Authorization": f"Bearer {user_token}"}
        
        # Test filtering by name
        response = await test_client.get(
            f"/api/clients?name={test_client_data['name']}", 
            headers=headers
        )
        data = response.json()
        
        assert response.status_code == 200
        assert data["success"] is True
        assert len(data["data"]) >= 1
        assert data["data"][0]["name"] == test_client_data["name"]
    
    @pytest.mark.asyncio
    async def test_get_client_by_id(self, test_client: AsyncClient, user_token, test_client_data):
        """Test getting a client by ID"""
        headers = {"Authorization": f"Bearer {user_token}"}
        
        response = await test_client.get(
            f"/api/clients/{test_client_data['id']}", 
            headers=headers
        )
        data = response.json()
        
        # Assert response
        assert response.status_code == 200
        assert data["success"] is True
        assert data["message"] == "Client retrieved successfully"
        assert data["data"]["id"] == test_client_data["id"]
        assert data["data"]["name"] == test_client_data["name"]
        assert data["data"]["email"] == test_client_data["email"]
    
    @pytest.mark.asyncio
    async def test_get_client_invalid_id(self, test_client: AsyncClient, user_token):
        """Test getting a client with an invalid ID"""
        headers = {"Authorization": f"Bearer {user_token}"}
        
        response = await test_client.get("/api/clients/invalidid", headers=headers)
        data = response.json()
        
        # Assert response
        assert response.status_code == 404
        assert "detail" in data
    
    @pytest.mark.asyncio
    async def test_update_client(self, test_client: AsyncClient, user_token, test_client_data):
        """Test updating a client"""
        headers = {"Authorization": f"Bearer {user_token}"}
        
        update_data = {
            "contactPerson": "Updated Contact Person",
            "phone": "+9999999999"
        }
        
        response = await test_client.put(
            f"/api/clients/{test_client_data['id']}", 
            json=update_data,
            headers=headers
        )
        data = response.json()
        
        # Assert response
        assert response.status_code == 200
        assert data["success"] is True
        assert data["message"] == "Client updated successfully"
        
        # Verify the update with a GET request
        response = await test_client.get(
            f"/api/clients/{test_client_data['id']}", 
            headers=headers
        )
        data = response.json()
        
        assert data["data"]["contactPerson"] == update_data["contactPerson"]
        assert data["data"]["phone"] == update_data["phone"]
    
    @pytest.mark.asyncio
    async def test_delete_client(self, test_client: AsyncClient, user_token, test_client_data):
        """Test soft deleting a client"""
        # Create a new client to delete since we need the test_client_data for other tests
        client_data = {
            "name": "Client To Delete",
            "contactPerson": "Delete Me",
            "email": "delete@example.com",
            "phone": "+1122334455"
        }
        
        headers = {"Authorization": f"Bearer {user_token}"}
        
        # Create client
        create_response = await test_client.post("/api/clients", json=client_data, headers=headers)
        create_data = create_response.json()
        client_id = create_data["data"]["id"]
        
        # Delete the client
        delete_response = await test_client.delete(f"/api/clients/{client_id}", headers=headers)
        delete_data = delete_response.json()
        
        # Assert delete response
        assert delete_response.status_code == 200
        assert delete_data["success"] is True
        assert delete_data["message"] == "Client deleted successfully"
        
        # Try to get the deleted client - it should be soft deleted
        get_response = await test_client.get(f"/api/clients/{client_id}", headers=headers)
        
        assert get_response.status_code == 404
    
    @pytest.mark.asyncio
    async def test_permanent_delete_client_admin(self, test_client: AsyncClient, admin_token, test_client_data):
        """Test permanently deleting a client as an admin"""
        # Create a new client to permanently delete
        client_data = {
            "name": "Client To Permanently Delete",
            "contactPerson": "Permanent Delete",
            "email": "permdelete@example.com",
            "phone": "+3344556677"
        }
        
        headers = {"Authorization": f"Bearer {admin_token}"}
        
        # Create client
        create_response = await test_client.post("/api/clients", json=client_data, headers=headers)
        create_data = create_response.json()
        client_id = create_data["data"]["id"]
        
        # Permanently delete the client
        delete_response = await test_client.delete(
            f"/api/clients/{client_id}/permanent", 
            headers=headers
        )
        delete_data = delete_response.json()
        
        # Assert delete response
        assert delete_response.status_code == 200
        assert delete_data["success"] is True
        assert delete_data["message"] == "Client permanently deleted"
    
    @pytest.mark.asyncio
    async def test_permanent_delete_client_non_admin(self, test_client: AsyncClient, user_token):
        """Test permanently deleting a client as a non-admin (should fail)"""
        # Create a new client to attempt to permanently delete
        client_data = {
            "name": "Client For Non-Admin Delete Attempt",
            "contactPerson": "Non Admin Delete",
            "email": "nonadmin@example.com",
            "phone": "+5566778899"
        }
        
        headers = {"Authorization": f"Bearer {user_token}"}
        
        # Create client
        create_response = await test_client.post("/api/clients", json=client_data, headers=headers)
        create_data = create_response.json()
        client_id = create_data["data"]["id"]
        
        # Attempt to permanently delete the client
        delete_response = await test_client.delete(
            f"/api/clients/{client_id}/permanent", 
            headers=headers
        )
        delete_data = delete_response.json()
        
        # Assert delete response - should be forbidden for non-admin
        assert delete_response.status_code == 403
        assert "Not enough permissions" in delete_data.get("detail", "")