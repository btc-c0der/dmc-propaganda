from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
import os
from dotenv import load_dotenv

# Import models
from auth.models import User
from clients.models import Client
from campaigns.models import Campaign

# Load environment variables
load_dotenv()

# MongoDB connection settings
MONGODB_URI = os.environ.get("MONGODB_URI", "mongodb://localhost:27017/dmc-propaganda")

async def init_db():
    """Initialize database connection"""
    # Create Motor client
    client = AsyncIOMotorClient(MONGODB_URI)
    
    # Initialize beanie with the document models
    await init_beanie(
        database=client.get_default_database(),
        document_models=[
            User,
            Client, 
            Campaign
        ]
    )
    
    return client