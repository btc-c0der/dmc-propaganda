from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import os
from dotenv import load_dotenv
from config.database import init_db

# Load environment variables
load_dotenv()

# Import routers
from auth.router import router as auth_router
from clients.router import router as clients_router
from campaigns.router import router as campaigns_router
from analytics.router import router as analytics_router

# Create FastAPI app
app = FastAPI(
    title="DMC Propaganda API",
    description="API for DMC Propaganda Marketing Campaign Management",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins in development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth_router, prefix="/api/auth", tags=["Authentication"])
app.include_router(clients_router, prefix="/api/clients", tags=["Clients"])
app.include_router(campaigns_router, prefix="/api/campaigns", tags=["Campaigns"])
app.include_router(analytics_router, prefix="/api/analytics", tags=["Analytics"])

@app.on_event("startup")
async def startup_event():
    """Initialize database connection when the application starts"""
    print("Initializing database connection...")
    await init_db()
    print("Database initialized successfully!")

@app.get("/")
async def root():
    """Root endpoint that returns API information"""
    return {
        "message": "DMC Propaganda API",
        "version": "1.0.0",
        "environment": os.environ.get("ENV", "development"),
    }

@app.get("/api")
async def api_root():
    """API root endpoint for health checks"""
    return {
        "status": "ok",
        "message": "API is running properly",
    }

if __name__ == "__main__":
    # Start the server with uvicorn
    uvicorn.run(
        "main:app", 
        host="0.0.0.0", 
        port=int(os.environ.get("PORT", 3000)),
        reload=True
    )