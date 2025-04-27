import pytest
import asyncio
from typing import AsyncGenerator, Dict, List
from datetime import datetime
from httpx import AsyncClient
from fastapi.testclient import TestClient
from beanie.odm.fields import PydanticObjectId
from pymongo import MongoClient
import os
import sys

# Add the parent directory to the path so we can import the app
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main import app
from auth.models import User, UserCreate
from clients.models import Client, Address, SocialMediaHandles
from campaigns.models import Campaign, TargetAudience, CampaignMetrics
from config.database import init_db

# Test database name - different from the main database
TEST_MONGODB_URI = "mongodb://localhost:27017/dmc-propaganda-test"

@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for the test session"""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

@pytest.fixture(scope="session")
async def setup_test_db():
    """Setup the test database"""
    # Override the MongoDB URI for tests
    os.environ["MONGODB_URI"] = TEST_MONGODB_URI
    await init_db()
    yield
    # Clean up after tests
    client = MongoClient(TEST_MONGODB_URI)
    client.drop_database("dmc-propaganda-test")

@pytest.fixture(scope="function")
async def clear_test_data():
    """Clear test data between tests"""
    client = MongoClient(TEST_MONGODB_URI)
    db = client.get_database()
    collections = ['users', 'clients', 'campaigns']
    
    for collection in collections:
        if collection in db.list_collection_names():
            db[collection].delete_many({})
    
    yield

@pytest.fixture
async def test_client(setup_test_db) -> AsyncGenerator[AsyncClient, None]:
    """Create a test client for FastAPI"""
    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client

@pytest.fixture
async def test_user() -> Dict:
    """Create a test user for authentication tests"""
    user_data = {
        "name": "Test User",
        "email": "test@example.com",
        "password": User.get_password_hash("password123"),
        "role": "user",
        "isActive": True,
        "lastLogin": datetime.utcnow(),
        "createdAt": datetime.utcnow(),
        "updatedAt": datetime.utcnow()
    }
    
    user = User(**user_data)
    await user.create()
    
    return {
        "id": str(user.id),
        "email": user.email,
        "password_plain": "password123",
        "role": user.role
    }

@pytest.fixture
async def test_admin() -> Dict:
    """Create a test admin user"""
    admin_data = {
        "name": "Admin User",
        "email": "admin@example.com",
        "password": User.get_password_hash("admin123"),
        "role": "admin",
        "isActive": True,
        "lastLogin": datetime.utcnow(),
        "createdAt": datetime.utcnow(),
        "updatedAt": datetime.utcnow()
    }
    
    admin = User(**admin_data)
    await admin.create()
    
    return {
        "id": str(admin.id),
        "email": admin.email,
        "password_plain": "admin123",
        "role": admin.role
    }

@pytest.fixture
async def test_client_data() -> Dict:
    """Create a test client record"""
    client_data = {
        "name": "Test Client Company",
        "contactPerson": "John Contact",
        "email": "contact@testclient.com",
        "phone": "+1234567890",
        "industry": "Technology",
        "website": "https://testclient.com",
        "address": Address(
            street="123 Test St",
            city="Test City",
            state="Test State",
            postalCode="12345",
            country="Test Country"
        ),
        "socialMediaHandles": SocialMediaHandles(
            facebook="testclient",
            instagram="testclient",
            twitter="testclient"
        ),
        "notes": "Test client for testing purposes",
        "isActive": True,
        "createdAt": datetime.utcnow(),
        "updatedAt": datetime.utcnow()
    }
    
    client = Client(**client_data)
    await client.create()
    
    return {
        "id": str(client.id),
        "name": client.name,
        "email": client.email
    }

@pytest.fixture
async def test_campaign_data(test_client_data) -> Dict:
    """Create a test campaign record"""
    client = await Client.get(test_client_data["id"])
    
    campaign_data = {
        "name": "Test Marketing Campaign",
        "client": client,
        "description": "A test campaign for testing purposes",
        "startDate": datetime.utcnow(),
        "endDate": datetime.utcnow().replace(year=datetime.utcnow().year + 1),
        "budget": 10000.0,
        "status": "active",
        "objectives": ["Increase brand awareness", "Generate leads"],
        "targetAudience": TargetAudience(
            demographics="25-45 years, professionals",
            interests=["technology", "marketing"],
            location="Global"
        ),
        "channels": ["social media", "email", "web"],
        "metrics": CampaignMetrics(
            impressions=5000,
            clicks=500,
            conversions=50,
            roi=2.5
        ),
        "isActive": True,
        "createdAt": datetime.utcnow(),
        "updatedAt": datetime.utcnow()
    }
    
    campaign = Campaign(**campaign_data)
    await campaign.create()
    
    return {
        "id": str(campaign.id),
        "name": campaign.name,
        "client_id": test_client_data["id"]
    }

@pytest.fixture
async def admin_token(test_client, test_admin) -> str:
    """Get a JWT token for an admin user"""
    response = await test_client.post(
        "/api/auth/login",
        data={
            "username": test_admin["email"],
            "password": test_admin["password_plain"]
        }
    )
    
    data = response.json()
    return data["data"]["token"]

@pytest.fixture
async def user_token(test_client, test_user) -> str:
    """Get a JWT token for a regular user"""
    response = await test_client.post(
        "/api/auth/login",
        data={
            "username": test_user["email"],
            "password": test_user["password_plain"]
        }
    )
    
    data = response.json()
    return data["data"]["token"]