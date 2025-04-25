# DMC Propaganda - G;RADIO Framework: How-To Guide

This comprehensive guide will help you navigate through the DMC Propaganda G;RADIO framework application, from setup to advanced features.

## Table of Contents
1. [Getting Started](#getting-started)
2. [Project Structure](#project-structure)
3. [API Usage](#api-usage)
4. [Authentication](#authentication)
5. [Client Management](#client-management)
6. [Campaign Management](#campaign-management)
7. [Testing](#testing)
8. [Educational Tools](#educational-tools)

## Getting Started

### Prerequisites
- Node.js (v16+)
- MongoDB (v4+)
- npm or yarn

### Installation

1. Clone the repository
```bash
git clone https://github.com/your-organization/dmc-propaganda.git
cd dmc-propaganda
```

2. Install dependencies
```bash
npm install
```

3. Configure environment variables
Create a `.env` file in the root directory with the following variables:
```
NODE_ENV=development
PORT=3000
MONGODB_URI=mongodb://localhost:27017/dmc-propaganda
JWT_SECRET=your_jwt_secret_key_here
JWT_EXPIRATION=7d
CORS_ORIGIN=*
```

4. Start MongoDB
Ensure MongoDB is running on your system.

5. Run the development server
```bash
npm run dev
```

6. Access the API
The API is now running at `http://localhost:3000`

## Project Structure

The application follows a micro-modules architecture:

```
src/
├── config/         # Configuration settings
├── core/           # Core framework utilities
├── interfaces/     # TypeScript interfaces and types
├── middleware/     # Express middleware
├── modules/        # Feature modules
│   ├── auth/       # Authentication & user management
│   ├── client/     # Client management
│   ├── campaign/   # Campaign management
│   ├── media/      # Media asset management
│   └── analytics/  # Analytics & reporting
├── tests/          # Test suites
└── utils/          # Utility functions
```

Each module follows a consistent structure:
- `controllers/` - Handle HTTP requests
- `models/` - Data models
- `services/` - Business logic
- `routes/` - API endpoints

## API Usage

### Base URL
- Development: `http://localhost:3000/api`
- Production: [Your production URL]/api

### Response Format
All API responses follow a standard format:

```json
{
  "success": true,
  "data": {}, // Response data
  "message": "Operation successful",
  "pagination": {} // Optional pagination details
}
```

Error responses:
```json
{
  "status": "error",
  "message": "Error message"
}
```

## Authentication

### Register a New User
```
POST /api/auth/register
```

Request body:
```json
{
  "name": "User Name",
  "email": "user@example.com",
  "password": "securePassword123"
}
```

### Login
```
POST /api/auth/login
```

Request body:
```json
{
  "email": "user@example.com",
  "password": "securePassword123"
}
```

Response:
```json
{
  "success": true,
  "data": {
    "user": {
      "_id": "userId",
      "name": "User Name",
      "email": "user@example.com",
      "role": "user"
    },
    "token": "JWT_TOKEN"
  },
  "message": "Login successful"
}
```

### Authentication in Requests
For protected endpoints, include the token in the Authorization header:

```
Authorization: Bearer YOUR_TOKEN_HERE
```

## Client Management

### Create a Client
```
POST /api/clients
```

Request body:
```json
{
  "name": "Client Company Name",
  "contactPerson": "Contact Name",
  "email": "contact@client.com",
  "phone": "+1234567890",
  "industry": "Marketing",
  "website": "https://client-website.com",
  "address": {
    "street": "Street Address",
    "city": "City",
    "state": "State",
    "postalCode": "12345",
    "country": "Country"
  }
}
```

### Get All Clients
```
GET /api/clients
```

Query parameters:
- `page`: Page number (default: 1)
- `limit`: Items per page (default: 10)
- `name`: Filter by name
- `industry`: Filter by industry

### Get Client by ID
```
GET /api/clients/:id
```

### Update Client
```
PUT /api/clients/:id
```

### Delete Client
```
DELETE /api/clients/:id
```

## Campaign Management

### Create a Campaign
```
POST /api/campaigns
```

Request body:
```json
{
  "name": "Campaign Name",
  "client": "clientId",
  "description": "Campaign description",
  "startDate": "2025-01-01T00:00:00Z",
  "endDate": "2025-03-01T00:00:00Z",
  "budget": 5000,
  "objectives": ["Increase brand awareness", "Generate leads"],
  "targetAudience": {
    "demographics": "25-45 years, professionals",
    "interests": ["technology", "finance"],
    "location": "Global"
  },
  "channels": ["social media", "email", "web"]
}
```

### Get Campaigns
```
GET /api/campaigns
```

Query parameters:
- `page`: Page number
- `limit`: Items per page
- `status`: Filter by status (draft, active, completed, cancelled)

### Get Client Campaigns
```
GET /api/campaigns/client/:clientId
```

### Update Campaign Status
```
PATCH /api/campaigns/:id/status
```

Request body:
```json
{
  "status": "active"
}
```

### Update Campaign Metrics
```
PATCH /api/campaigns/:id/metrics
```

Request body:
```json
{
  "metrics": {
    "impressions": 10000,
    "clicks": 500,
    "conversions": 50,
    "roi": 2.5
  }
}
```

## Testing

Run the test suite:
```bash
npm test
```

Running specific tests:
```bash
npm test -- -t "Auth Service"
```

## Educational Tools

The project includes educational tools in the `tmp` directory:

### Spain to Brazil Map
Run the Python script to generate a map:
```bash
python tmp/spain_brazil_map.py
```

### Interactive Geography Game for Kids
Launch the turtle-based educational game:
```bash
python tmp/enhanced_turtle_map_game.py
```

This interactive game teaches children about geography and cultural connections between Spain and Brazil.

---

For more detailed information about specific components, refer to the inline code documentation.