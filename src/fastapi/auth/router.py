from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from datetime import datetime
from typing import Any, Dict
from .models import User, UserCreate, UserResponse, Token
from .jwt import create_access_token, get_current_user

router = APIRouter()

@router.post("/register", response_model=Dict[str, Any], status_code=status.HTTP_201_CREATED)
async def register(user_data: UserCreate):
    """Register a new user"""
    # Check if email already exists
    existing_user = await User.find_one(User.email == user_data.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Create new user with hashed password
    hashed_password = User.get_password_hash(user_data.password)
    
    new_user = User(
        name=user_data.name,
        email=user_data.email,
        password=hashed_password,
        role=user_data.role
    )
    
    # Save user to database
    await new_user.create()
    
    # Generate token
    token_data = {
        "id": str(new_user.id),
        "email": new_user.email,
        "role": new_user.role
    }
    access_token = create_access_token(token_data)
    
    # Create response
    user_response = {
        "success": True,
        "data": {
            "user": {
                "id": str(new_user.id),
                "name": new_user.name,
                "email": new_user.email,
                "role": new_user.role
            },
            "token": access_token
        },
        "message": "User registered successfully"
    }
    
    return user_response

@router.post("/login", response_model=Dict[str, Any])
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    """Authenticate user and return JWT token"""
    # Find user by email
    user = await User.find_one(User.email == form_data.username)
    
    # Check if user exists and password is correct
    if not user or not user.verify_password(form_data.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Bearer"}
        )
    
    # Check if user is active
    if not user.isActive:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Account is inactive"
        )
    
    # Update last login timestamp
    user.lastLogin = datetime.utcnow()
    await user.save()
    
    # Generate token
    token_data = {
        "id": str(user.id),
        "email": user.email,
        "role": user.role
    }
    access_token = create_access_token(token_data)
    
    # Create response
    auth_response = {
        "success": True,
        "data": {
            "user": {
                "id": str(user.id),
                "name": user.name,
                "email": user.email,
                "role": user.role,
                "lastLogin": user.lastLogin
            },
            "token": access_token
        },
        "message": "Login successful"
    }
    
    return auth_response

@router.get("/profile", response_model=Dict[str, Any])
async def get_profile(current_user: User = Depends(get_current_user)):
    """Get current user profile"""
    # Create response
    profile_response = {
        "success": True,
        "data": {
            "id": str(current_user.id),
            "name": current_user.name,
            "email": current_user.email,
            "role": current_user.role,
            "lastLogin": current_user.lastLogin,
            "createdAt": current_user.createdAt
        },
        "message": "User profile retrieved successfully"
    }
    
    return profile_response