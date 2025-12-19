# Better Auth Integration Guide for Developers

## Overview
This guide provides instructions for developers who need to work with the Better Auth integration in the existing FastAPI (Python) backend and Docusaurus (React) frontend with Neon Serverless Postgres.

## Architecture Overview

### System Components
- **Frontend**: Docusaurus React application with authentication pages
- **Backend**: FastAPI API with Better Auth proxy and application endpoints
- **Authentication**: Better Auth Node.js service (externally managed)
- **Database**: Neon Serverless Postgres with Better Auth and application tables

### Data Flow
```
Frontend (React) -> FastAPI (Python) -> Better Auth (Node.js) -> Neon Postgres
                                    -> Application APIs (Python) -> Application Tables
```

## Setting Up Development Environment

### Prerequisites
- Python 3.11+ with pip
- Node.js 18+ with npm/pnpm
- PostgreSQL-compatible database (Neon Serverless Postgres)
- Docusaurus project already set up

### Backend Setup
1. Install Python dependencies:
```bash
pip install fastapi uvicorn python-multipart asyncpg python-multipart python-jose[cryptography] passlib[bcrypt] python-dotenv
```

2. Create `.env` file in backend directory:
```bash
DATABASE_URL=your_neon_postgres_connection_string
BETTER_AUTH_SECRET=generate_a_strong_secret
BETTER_AUTH_URL=http://localhost:8000
BETTER_AUTH_TRUSTED_ORIGINS=http://localhost:3000,http://localhost:8000
```

### Frontend Setup
1. Install Better Auth client:
```bash
npm install better-auth
```

2. Create auth client configuration in `frontend/src/components/auth/auth-client.js`

## Adding New Authentication Features

### Backend Endpoints
1. Create new endpoints in the appropriate API module (e.g., `api/v1/profile.py`)
2. Use the existing authentication patterns with `get_current_user` and `is_endpoint_accessible`
3. Ensure RAG endpoints remain accessible to anonymous users

### Frontend Components
1. Create new components in `frontend/src/components/auth/`
2. Use the existing auth client for authentication flows
3. Follow the existing patterns for session management

### Database Migrations
1. Update the `database_migrations.py` script if new tables are needed
2. Use asyncpg for database operations
3. Follow the existing connection pool patterns

## Working with User Profiles

### Creating User Profiles
```python
# In your API endpoint
current_user = await get_current_user(request)
user_id = current_user.get('user', {}).get('id')

# Validate consent before storing background information
if not profile_data.consent_given and (profile_data.software_background or profile_data.hardware_background):
    raise HTTPException(status_code=400, detail="Consent must be given to store background information")
```

### Updating User Profiles
- Always validate consent before updating background information
- Use the existing profile API as a reference
- Ensure proper error handling and validation

## Testing Authentication Features

### Unit Tests
- Use FastAPI TestClient for backend API tests
- Mock Better Auth service for isolated testing
- Test both authenticated and unauthenticated flows

### Integration Tests
- Test the complete authentication flow
- Verify RAG endpoints remain accessible to anonymous users
- Test consent validation and privacy rules

## Security Considerations

### Session Management
- Sessions are managed by Better Auth
- Use the provided middleware for session validation
- Never store sensitive information in client-side storage

### Data Privacy
- Always validate user consent before storing personal information
- Follow the privacy rules documented in session-privacy.md
- Log authentication events while preserving privacy

### API Security
- Use proper authentication checks for protected endpoints
- Validate input data thoroughly
- Implement rate limiting where appropriate

## Troubleshooting Common Issues

### Authentication Endpoints Return 404
- Verify the catch-all route `/auth/{path:path}` is properly configured
- Check that the Better Auth service is running and accessible

### Database Migrations Fail
- Ensure your DATABASE_URL is correct
- Verify Neon Postgres connection settings
- Check that the database user has proper permissions

### Sessions Don't Persist
- Verify cookie settings are configured properly
- Check CORS configuration matches your frontend domain
- Ensure the Better Auth service is properly configured

### RAG Endpoints Become Blocked
- Verify that authentication middleware doesn't intercept RAG endpoints
- Check the `is_endpoint_accessible` function logic
- Ensure RAG endpoints are properly configured as public

## Deployment Considerations

### Environment Variables
- Set proper production values for all environment variables
- Use secure secrets for BETTER_AUTH_SECRET
- Configure proper domains for CORS and trusted origins

### Database
- Run database migrations before deployment
- Ensure proper backup and recovery procedures
- Monitor database connection pool usage

### Security
- Enable HTTPS in production
- Configure proper security headers
- Implement monitoring and alerting for authentication events

## API Reference

### Authentication Endpoints
- `POST /auth/signin` - User sign in
- `POST /auth/signup` - User registration
- `POST /auth/signout` - User sign out
- `GET /auth/session` - Get current session

### User Profile Endpoints
- `POST /api/v1/profile` - Create/update user profile
- `GET /api/v1/profile` - Get user profile

### RAG Endpoints (Public)
- `POST /api/v1/query` - Query the RAG system
- `POST /api/v1/select` - Select relevant documents

## Future Enhancements

### Planned Features
- Social login integration
- Password reset functionality
- User preferences and settings
- Admin panel for user management

### Monitoring and Analytics
- Authentication event logging
- User engagement metrics
- Performance monitoring for auth flows
- Privacy compliance reporting

## Support and Resources

### Documentation
- Better Auth official documentation
- FastAPI documentation
- Neon Postgres documentation
- Docusaurus documentation

### Contact
- For authentication issues: Check the auth logs first
- For database issues: Verify connection settings
- For frontend issues: Check browser console for errors