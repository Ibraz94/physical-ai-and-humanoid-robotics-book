# Better Auth Integration Documentation

## Overview
This document describes the Better Auth integration with the FastAPI backend and Docusaurus frontend. The integration provides email/password authentication while maintaining separation between authentication and RAG functionality.

## Architecture

### Backend Architecture
- **Better Auth Service**: Node.js-based authentication service
- **FastAPI Backend**: Python API that proxies authentication requests to Better Auth
- **Database**: Neon Serverless Postgres with Better Auth managing user/session tables
- **Application Tables**: Separate `user_profiles` table for application-specific data

### Frontend Architecture
- **Docusaurus React**: Frontend framework with authentication components
- **Better Auth Client**: JavaScript client library for authentication flows
- **Auth Pages**: Signup and signin pages with background information collection

## Environment Variables

### Backend (.env)
```bash
# Better Auth Configuration
BETTER_AUTH_URL=http://localhost:8000
BETTER_AUTH_SECRET=your-secret-key-here
BETTER_AUTH_COOKIE_NAME=better-auth-session

# Database Configuration
DATABASE_URL=your-neon-postgres-connection-string

# Additional Configuration
BETTER_AUTH_HOST=localhost
BETTER_AUTH_PORT=8000
```

### Frontend (.env)
```bash
REACT_APP_BETTER_AUTH_URL=http://localhost:8000
```

## API Endpoints

### Authentication Endpoints
- `POST /auth/signin` - User sign in
- `POST /auth/signup` - User registration
- `POST /auth/signout` - User sign out
- `GET /auth/session` - Get current session

### User Profile Endpoints
- `POST /api/v1/profile` - Create/update user profile with consent
- `GET /api/v1/profile` - Get user profile (authenticated users only)

### RAG Endpoints (Unchanged)
- `POST /api/v1/query` - Query the RAG system (accessible to all)
- `POST /api/v1/select` - Select relevant documents (accessible to all)

## MCP Server Verification

### Better Auth MCP Server
- Verified Better Auth integration patterns with FastAPI
- Confirmed database adapter compatibility with Neon Postgres
- Validated session management and security best practices

### Context7 MCP Server
- Verified FastAPI authentication patterns
- Confirmed OAuth2 password flow implementation
- Validated dependency injection for current user

## Configuration Files

### auth.config.ts
Better Auth configuration with:
- Neon database adapter
- Email/password authentication
- Session configuration
- Custom user fields for background information
- CORS configuration for frontend integration

## Integration Notes

### Session Isolation
- RAG endpoints remain accessible to anonymous users
- Authentication flows do not interfere with core functionality
- Session validation is optional for RAG endpoints
- User-specific features are available only when authenticated