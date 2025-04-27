# Authentication Module (AUTH)

## Overview
The authentication module provides secure user registration, login, and profile management for the DMC Propaganda system. It is built with FastAPI and uses MongoDB (Beanie ODM) for user data storage. Authentication is handled via JWT tokens, and the module supports role-based access control.

## Features
- **User Registration**: Registers new users, checks for unique email, hashes passwords with bcrypt, and returns a JWT token.
- **User Login**: Authenticates users, verifies credentials, updates last login timestamp, and returns a JWT token.
- **Profile Retrieval**: Returns the current user's profile information (JWT required).
- **Role-Based Access Control**: Supports user roles (`user`, `manager`, `admin`) and restricts endpoints as needed.
- **Password Security**: Passwords are hashed using passlib's bcrypt.

## Endpoints
- `POST /api/auth/register` — Register a new user
- `POST /api/auth/login` — Authenticate and receive a JWT token
- `GET /api/auth/profile` — Retrieve the current user's profile (requires JWT)

## JWT Authentication
- JWT tokens include user id, email, and role.
- Tokens are validated on each request.
- Middleware is provided for role-based endpoint protection.

## User Model
- Fields: `name`, `email`, `password` (hashed), `role`, `isActive`, `lastLogin`, `createdAt`, `updatedAt`
- Passwords are never returned in API responses.

## Example Usage
- Register a user, then use the returned token to authenticate further requests.
- Protect sensitive endpoints by requiring specific roles using the provided middleware.

---
For implementation details, see `src/fastapi/auth/` (router.py, models.py, jwt.py).
