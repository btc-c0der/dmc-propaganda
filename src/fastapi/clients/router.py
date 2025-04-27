from fastapi import APIRouter, Depends, HTTPException, status, Query
from typing import List, Dict, Any, Optional
from datetime import datetime
from .models import Client, ClientCreate, ClientUpdate, ClientResponse
from auth.jwt import get_current_user, role_required
from auth.models import User

router = APIRouter()

@router.post("/", response_model=Dict[str, Any], status_code=status.HTTP_201_CREATED)
async def create_client(
    client_data: ClientCreate,
    current_user: User = Depends(get_current_user)
):
    """Create a new client"""
    # Check if client with same name already exists
    existing_client = await Client.find_one(Client.name == client_data.name)
    if existing_client:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A client with this name already exists"
        )
    
    # Create new client
    new_client = Client(**client_data.dict())
    await new_client.create()
    
    # Create response
    response = {
        "success": True,
        "data": {
            "id": str(new_client.id),
            "name": new_client.name,
            "contactPerson": new_client.contactPerson,
            "email": new_client.email,
            "phone": new_client.phone,
            "industry": new_client.industry,
            "createdAt": new_client.createdAt,
        },
        "message": "Client created successfully"
    }
    
    return response

@router.get("/", response_model=Dict[str, Any])
async def get_clients(
    page: int = Query(1, ge=1, description="Page number"),
    limit: int = Query(10, ge=1, le=100, description="Items per page"),
    name: Optional[str] = None,
    industry: Optional[str] = None,
    current_user: User = Depends(get_current_user)
):
    """Get all clients with filtering and pagination"""
    # Build query filter
    query = {}
    if name:
        query["name"] = {"$regex": name, "$options": "i"}
    if industry:
        query["industry"] = industry
    query["isActive"] = True
    
    # Calculate pagination
    skip = (page - 1) * limit
    
    # Get clients with pagination
    clients = await Client.find(query).skip(skip).limit(limit).to_list()
    
    # Get total count
    total = await Client.count_documents(query)
    
    # Create response
    response = {
        "success": True,
        "data": [
            {
                "id": str(client.id),
                "name": client.name,
                "contactPerson": client.contactPerson,
                "email": client.email,
                "phone": client.phone,
                "industry": client.industry,
                "logo": client.logo,
                "website": client.website,
                "createdAt": client.createdAt
            }
            for client in clients
        ],
        "message": "Clients retrieved successfully",
        "pagination": {
            "page": page,
            "limit": limit,
            "total": total,
            "pages": (total + limit - 1) // limit  # ceiling division
        }
    }
    
    return response

@router.get("/{client_id}", response_model=Dict[str, Any])
async def get_client_by_id(
    client_id: str,
    current_user: User = Depends(get_current_user)
):
    """Get a client by ID"""
    client = await Client.get(client_id)
    if not client or not client.isActive:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Client not found"
        )
    
    # Create response
    response = {
        "success": True,
        "data": {
            "id": str(client.id),
            "name": client.name,
            "contactPerson": client.contactPerson,
            "email": client.email,
            "phone": client.phone,
            "address": client.address,
            "industry": client.industry,
            "logo": client.logo,
            "website": client.website,
            "socialMediaHandles": client.socialMediaHandles,
            "notes": client.notes,
            "createdAt": client.createdAt,
            "updatedAt": client.updatedAt
        },
        "message": "Client retrieved successfully"
    }
    
    return response

@router.put("/{client_id}", response_model=Dict[str, Any])
async def update_client(
    client_id: str,
    client_data: ClientUpdate,
    current_user: User = Depends(get_current_user)
):
    """Update a client"""
    client = await Client.get(client_id)
    if not client or not client.isActive:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Client not found"
        )
    
    # Check if name is being updated and if it's already taken
    if client_data.name and client_data.name != client.name:
        existing_client = await Client.find_one(Client.name == client_data.name)
        if existing_client and str(existing_client.id) != client_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="A client with this name already exists"
            )
    
    # Update client
    update_data = client_data.dict(exclude_unset=True)
    update_data["updatedAt"] = datetime.utcnow()
    
    for field, value in update_data.items():
        setattr(client, field, value)
    
    await client.save()
    
    # Create response
    response = {
        "success": True,
        "data": {
            "id": str(client.id),
            "name": client.name,
            "contactPerson": client.contactPerson,
            "email": client.email,
            "updatedAt": client.updatedAt
        },
        "message": "Client updated successfully"
    }
    
    return response

@router.delete("/{client_id}", response_model=Dict[str, Any])
async def delete_client(
    client_id: str,
    current_user: User = Depends(get_current_user)
):
    """Soft delete a client"""
    client = await Client.get(client_id)
    if not client or not client.isActive:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Client not found"
        )
    
    # Soft delete (set isActive to False)
    client.isActive = False
    client.updatedAt = datetime.utcnow()
    await client.save()
    
    # Create response
    response = {
        "success": True,
        "data": None,
        "message": "Client deleted successfully"
    }
    
    return response

@router.delete("/{client_id}/permanent", response_model=Dict[str, Any])
async def permanent_delete_client(
    client_id: str,
    current_user: User = Depends(role_required(["admin"]))
):
    """Permanently delete a client (admin only)"""
    client = await Client.get(client_id)
    if not client:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Client not found"
        )
    
    # Permanently delete
    await client.delete()
    
    # Create response
    response = {
        "success": True,
        "data": None,
        "message": "Client permanently deleted"
    }
    
    return response