# DMC Propaganda - G;RADIO Framework Implementation

A professional-grade web application for DMC Propaganda from Campinas SP, Brasil using the G;RADIO framework with micro modules architecture and test-driven development.

## Project Overview

This project provides a comprehensive marketing campaign management system for DMC Propaganda, implementing:

- Micro-modules architecture for scalable code organization
- Test-driven development approach
- RESTful API design patterns
- JWT-based authentication & authorization
- Comprehensive client and campaign management
- Educational tools for children through the Kids Bless initiative

## Documentation

We've prepared comprehensive documentation to help you navigate the project:

- [How-To Guide](HOW-TO-GUIDE.md) - Detailed instructions for setting up and using the application
- [Contribution Guidelines](CONTRIBUTE.md) - Guidelines for developers who want to contribute
- [Kids Bless Educational Tools](KIDS-BLESS.md) - Information about our educational components for children

## Technologies Used

- Node.js & Express.js
- TypeScript
- MongoDB with Mongoose ODM
- JWT for authentication
- Jest for testing
- G;RADIO architectural patterns
- Python for educational tools

## Project Structure

The project follows a micro-modules architecture, with each domain having its own encapsulated functionality:

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
tmp/                # Educational tools for Kids Bless initiative
```

Each module follows a consistent structure:
- `controllers/` - Handle HTTP requests
- `models/` - Data models
- `services/` - Business logic
- `routes/` - API endpoints

## Getting Started

### Prerequisites

- Node.js (v16+)
- MongoDB (v4+)

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

3. Create a `.env` file in the root directory with the following variables:
```
NODE_ENV=development
PORT=3000
MONGODB_URI=mongodb://localhost:27017/dmc-propaganda
JWT_SECRET=your_jwt_secret_key_here
JWT_EXPIRATION=7d
CORS_ORIGIN=*
```

4. Start the development server
```bash
npm run dev
```

### Running Tests

```bash
npm test
```

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

### Educational Components
- Interactive geography games for children
- Cultural exchange educational tools
- Map visualizations for educational purposes

## API Endpoints

Refer to our [How-To Guide](HOW-TO-GUIDE.md) for a complete list of API endpoints and their usage.

## Kids Bless Initiative

![Kids Bless](docs/images/kids_bless_logo.png) <!-- Add this image if available -->

The Kids Bless initiative is our educational arm, creating interactive tools to help children learn about geography, culture, and international connections. See [KIDS-BLESS.md](KIDS-BLESS.md) for more information.

## Contributing

We welcome contributions! Please read our [Contribution Guidelines](CONTRIBUTE.md) for details on how to submit pull requests, coding standards, and more.

## License

This project is licensed under the ISC License.

## About DMC Propaganda

DMC Propaganda is a marketing agency based in Campinas SP, Brasil. Visit their official website at [https://www.dmcpropaganda.com.br/](https://www.dmcpropaganda.com.br/)