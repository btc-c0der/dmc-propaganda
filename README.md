# DMC Propaganda - Marketing Campaign Management System

A professional-grade web application for DMC Propaganda from Campinas SP, Brasil using FastAPI and Gradio with a modular architecture and MongoDB database.

## Project Overview

This project provides a comprehensive marketing campaign management system for DMC Propaganda, implementing:

- FastAPI backend with MongoDB database
- Gradio web interface for intuitive user experience
- Advanced marketing analytics models in Python
- RESTful API with JWT authentication & authorization
- Comprehensive client and campaign management
- Educational tools for children through the Kids Bless initiative

## Documentation

We've prepared comprehensive documentation to help you navigate the project:

- [How-To Guide](HOW-TO-GUIDE.md) - Detailed instructions for setting up and using the application
- [Contribution Guidelines](CONTRIBUTE.md) - Guidelines for developers who want to contribute
- [Kids Bless Educational Tools](KIDS-BLESS.md) - Information about our educational components for children

## Technologies Used

- **Backend**: FastAPI, MongoDB (with Beanie ODM)
- **Frontend**: Gradio
- **Authentication**: JWT, OAuth2
- **Analytics**: Python data science ecosystem (Pandas, NumPy, PyMC)
- **API Documentation**: FastAPI Swagger/OpenAPI

## Project Structure

The project follows a modular architecture:

```
src/
├── fastapi/           # FastAPI backend
│   ├── main.py        # Main FastAPI application
│   ├── auth/          # Authentication module 
│   ├── clients/       # Client management module
│   ├── campaigns/     # Campaign management module
│   ├── analytics/     # Analytics module
│   └── config/        # Configuration
│
├── gradio/            # Gradio frontend
│   ├── app.py         # Main Gradio application
│   ├── server.py      # Server startup script
│   └── marketing_models/ # Advanced analytics models
```

## Getting Started

### Prerequisites

- Python 3.10+
- MongoDB 4.0+

### Installation

1. Clone the repository
```bash
git clone https://github.com/your-organization/dmc-propaganda.git
cd dmc-propaganda
```

2. Run the start script
```bash
python start.py
```

This will:
- Install all required dependencies
- Initialize the database connection
- Start the FastAPI backend and Gradio frontend

3. Access the application
   - Gradio interface: http://localhost:7860
   - FastAPI backend: http://localhost:3000
   - API documentation: http://localhost:3000/docs

## Key Features

### Marketing Campaign Management
- Complete client management system
- Campaign creation and tracking
- Team collaboration features
- Performance metrics and analytics

### Authentication & Authorization
- Secure JWT-based authentication
- Role-based access control
- Password encryption
- Session management

### Advanced Marketing Analytics
- Media mix modeling
- Customer lifetime value analysis
- Customer segmentation
- Performance reporting

### Educational Components
- Interactive geography games for children
- Cultural exchange educational tools
- Map visualizations for educational purposes

## API Endpoints

The FastAPI backend provides a comprehensive set of endpoints:

- **/api/auth** - Authentication (register, login, profile)
- **/api/clients** - Client management (CRUD operations)
- **/api/campaigns** - Campaign management (CRUD operations, team management, metrics)
- **/api/analytics** - Analytics endpoints (campaign metrics, summary statistics)

Full API documentation is available at http://localhost:3000/docs when the server is running.

## Contributing

We welcome contributions! Please read our [Contribution Guidelines](CONTRIBUTE.md) for details on how to submit pull requests, coding standards, and more.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## About DMC Propaganda

DMC Propaganda is a marketing agency based in Campinas, São Paulo, Brazil, specializing in integrated marketing campaigns, digital strategy, and educational outreach through the Kids Bless initiative.