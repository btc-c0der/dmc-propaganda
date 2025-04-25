# Contributing to DMC Propaganda G;RADIO Framework

Thank you for your interest in contributing to our project! We welcome contributions from developers of all skill levels.

## Table of Contents
1. [Code of Conduct](#code-of-conduct)
2. [Getting Started](#getting-started)
3. [Development Workflow](#development-workflow)
4. [Pull Request Process](#pull-request-process)
5. [Coding Standards](#coding-standards)
6. [Testing Guidelines](#testing-guidelines)
7. [Documentation](#documentation)
8. [Educational Components](#educational-components)

## Code of Conduct

This project adheres to a Code of Conduct that all contributors are expected to follow. By participating, you agree to maintain:

- Respectful and inclusive language
- Acceptance of constructive criticism
- Focus on what is best for the community
- Empathy toward other community members

## Getting Started

### Prerequisites
- Node.js (v16+)
- MongoDB (v4+)
- Git

### Setting Up Development Environment

1. Fork the repository on GitHub
2. Clone your forked repository
   ```bash
   git clone https://github.com/YOUR-USERNAME/dmc-propaganda.git
   cd dmc-propaganda
   ```

3. Install dependencies
   ```bash
   npm install
   ```

4. Set up environment variables (copy from `.env.example`)
   ```bash
   cp .env.example .env
   ```

5. Run development server
   ```bash
   npm run dev
   ```

## Development Workflow

We follow a feature branch workflow:

1. Create a new branch for each feature/fix
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. Make your changes
3. Commit with meaningful messages
   ```bash
   git commit -m "feat: add new feature for client management"
   ```
   
   We follow the [Conventional Commits](https://www.conventionalcommits.org/) specification.

4. Push to your forked repository
   ```bash
   git push origin feature/your-feature-name
   ```

5. Create a Pull Request

## Pull Request Process

1. Ensure your code follows our coding standards
2. Update documentation as needed
3. Include tests that validate your changes
4. The PR should work in all targeted environments
5. Obtain approval from at least one maintainer
6. Your PR will be merged by a maintainer once approved

## Coding Standards

We follow a strict set of coding standards:

### TypeScript

- Use TypeScript for all new code
- Maintain strict typing
- Follow interface-first design

### Naming Conventions

- **Files**: lowercase with hyphens (e.g., `auth-service.ts`)
- **Classes**: PascalCase (e.g., `AuthService`)
- **Interfaces**: PascalCase with "I" prefix (e.g., `IUserModel`)
- **Variables & Functions**: camelCase (e.g., `getUserById`)
- **Constants**: UPPERCASE_WITH_UNDERSCORES

### Code Structure

- Follow the micro-modules architecture
- Each module should be self-contained
- Maintain separation of concerns

## Testing Guidelines

### Unit Testing

- All services and utilities must have unit tests
- Aim for at least 70% code coverage
- Use Jest mocks for external dependencies

### Integration Testing

- Test API endpoints with supertest
- Verify database operations with a test database
- Test authentication flows end-to-end

### Running Tests
```bash
# Run all tests
npm test

# Run specific tests
npm test -- -t "Auth Service"

# Generate coverage report
npm test -- --coverage
```

## Documentation

Good documentation is crucial for the project's success:

- Document all public APIs and functions
- Keep README.md up to date
- Update HOW-TO-GUIDE.md for new features
- Add JSDoc comments to all functions

Example JSDoc:
```typescript
/**
 * Authenticates a user with email and password
 * 
 * @param {LoginInput} credentials - User login credentials
 * @returns {Promise<AuthResponse>} - Authentication response with user data and token
 * @throws {ApiError} - If credentials are invalid
 */
async login(credentials: LoginInput): Promise<AuthResponse> {
  // Implementation
}
```

## Educational Components

Our project includes educational tools for children. If you're contributing to these components:

### Python Educational Tools

- Focus on visual learning and interactivity
- Maintain age-appropriate content (target age: 7-12)
- Ensure educational accuracy of geography and cultural information
- Follow PEP 8 style guide for Python code
- Test on multiple platforms (Windows, macOS, Linux)

### Creating New Educational Components

If you're adding a new educational tool:

1. Place it in the `tmp` directory
2. Include comprehensive comments
3. Document it in KIDS-BLESS.md
4. Create a simple installation guide

---

Thank you for contributing to the DMC Propaganda G;RADIO Framework! Your efforts help us create better software and educational tools for everyone.