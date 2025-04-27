from beanie import Document
from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from datetime import datetime
from passlib.context import CryptContext

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class User(Document):
    """User model for authentication and user management"""
    name: str
    email: EmailStr = Field(unique=True, index=True)
    password: str
    role: str = "user"  # user, manager, admin
    isActive: bool = True
    lastLogin: Optional[datetime] = None
    createdAt: datetime = Field(default_factory=datetime.utcnow)
    updatedAt: datetime = Field(default_factory=datetime.utcnow)
    
    class Settings:
        name = "users"
        
    def verify_password(self, plain_password: str) -> bool:
        """Verify password against hashed password"""
        return pwd_context.verify(plain_password, self.password)
    
    @classmethod
    def get_password_hash(cls, password: str) -> str:
        """Hash a password"""
        return pwd_context.hash(password)
    
    # Exclude password when converting to dict/json
    class Config:
        json_encoders = {
            datetime: lambda dt: dt.isoformat()
        }
        schema_extra = {
            "example": {
                "name": "John Doe",
                "email": "john@example.com",
                "role": "user"
            }
        }
        
# Auth schemas for request/response
class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str
    role: Optional[str] = "user"
    
class UserUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    role: Optional[str] = None
    isActive: Optional[bool] = None
    
class UserResponse(BaseModel):
    id: str
    name: str
    email: EmailStr
    role: str
    isActive: bool
    lastLogin: Optional[datetime] = None
    createdAt: datetime
    
class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    
class TokenData(BaseModel):
    id: str
    email: EmailStr
    role: str