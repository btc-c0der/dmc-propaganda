import pytest
from httpx import AsyncClient
import json
from datetime import datetime

# Tests for authentication endpoints
class TestAuth:
    
    @pytest.mark.asyncio
    async def test_register_success(self, test_client: AsyncClient, clear_test_data):
        """Test successful user registration"""
        user_data = {
            "name": "New User",
            "email": "newuser@example.com",
            "password": "password123"
        }
        
        response = await test_client.post("/api/auth/register", json=user_data)
        data = response.json()
        
        # Assert response
        assert response.status_code == 201
        assert data["success"] is True
        assert data["message"] == "User registered successfully"
        assert data["data"]["user"]["name"] == user_data["name"]
        assert data["data"]["user"]["email"] == user_data["email"]
        assert "token" in data["data"]
    
    @pytest.mark.asyncio
    async def test_register_duplicate_email(self, test_client: AsyncClient, test_user):
        """Test registration with an email that already exists"""
        user_data = {
            "name": "Duplicate User",
            "email": test_user["email"],  # Using the same email as the existing test user
            "password": "password123"
        }
        
        response = await test_client.post("/api/auth/register", json=user_data)
        data = response.json()
        
        # Assert response
        assert response.status_code == 400
        assert "Email already registered" in data.get("detail", "")
    
    @pytest.mark.asyncio
    async def test_login_success(self, test_client: AsyncClient, test_user):
        """Test successful login with valid credentials"""
        login_data = {
            "username": test_user["email"],
            "password": test_user["password_plain"]
        }
        
        response = await test_client.post("/api/auth/login", data=login_data)
        data = response.json()
        
        # Assert response
        assert response.status_code == 200
        assert data["success"] is True
        assert data["message"] == "Login successful"
        assert data["data"]["user"]["email"] == test_user["email"]
        assert "token" in data["data"]
        assert data["data"]["token"] != ""
    
    @pytest.mark.asyncio
    async def test_login_invalid_credentials(self, test_client: AsyncClient, test_user):
        """Test login with invalid credentials"""
        login_data = {
            "username": test_user["email"],
            "password": "wrongpassword"
        }
        
        response = await test_client.post("/api/auth/login", data=login_data)
        data = response.json()
        
        # Assert response
        assert response.status_code == 401
        assert "Invalid credentials" in data.get("detail", "")
    
    @pytest.mark.asyncio
    async def test_login_nonexistent_user(self, test_client: AsyncClient):
        """Test login with a non-existent user"""
        login_data = {
            "username": "nonexistent@example.com",
            "password": "password123"
        }
        
        response = await test_client.post("/api/auth/login", data=login_data)
        data = response.json()
        
        # Assert response
        assert response.status_code == 401
        assert "Invalid credentials" in data.get("detail", "")
    
    @pytest.mark.asyncio
    async def test_get_profile(self, test_client: AsyncClient, user_token):
        """Test getting user profile with a valid token"""
        headers = {"Authorization": f"Bearer {user_token}"}
        
        response = await test_client.get("/api/auth/profile", headers=headers)
        data = response.json()
        
        # Assert response
        assert response.status_code == 200
        assert data["success"] is True
        assert data["message"] == "User profile retrieved successfully"
        assert "id" in data["data"]
        assert "name" in data["data"]
        assert "email" in data["data"]
        assert "role" in data["data"]
    
    @pytest.mark.asyncio
    async def test_get_profile_invalid_token(self, test_client: AsyncClient):
        """Test getting user profile with an invalid token"""
        headers = {"Authorization": "Bearer invalidtoken"}
        
        response = await test_client.get("/api/auth/profile", headers=headers)
        data = response.json()
        
        # Assert response
        assert response.status_code == 401
        assert "Could not validate credentials" in data.get("detail", "")
    
    @pytest.mark.asyncio
    async def test_get_profile_no_token(self, test_client: AsyncClient):
        """Test getting user profile without a token"""
        response = await test_client.get("/api/auth/profile")
        data = response.json()
        
        # Assert response
        assert response.status_code == 401
        assert "Not authenticated" in data.get("detail", "")