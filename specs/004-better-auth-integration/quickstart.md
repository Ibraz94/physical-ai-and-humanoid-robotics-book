# Quickstart Guide: Better Auth Integration

## Prerequisites

- Python 3.11+ with pip
- Node.js 18+ with npm/pnpm
- PostgreSQL-compatible database (Neon Serverless Postgres)
- Docusaurus project already set up

## Installation

### Backend Setup (FastAPI)

1. Install required Python packages:
```bash
pip install fastapi uvicorn python-multipart
```

2. Install Better Auth (via Node.js):
```bash
npm install better-auth @better-auth/cli
```

3. Set up environment variables:
```bash
# .env file
DATABASE_URL="your-neon-postgres-connection-string"
BETTER_AUTH_SECRET="your-secret-key-here"
BETTER_AUTH_URL="http://localhost:8000"
```

### Frontend Setup (Docusaurus)

1. Install Better Auth client:
```bash
npm install better-auth
```

## Configuration

### Backend Configuration

1. Create authentication handler in FastAPI:
```python
# backend/app/auth_handler.py
from fastapi import FastAPI, Request, Response
import asyncio
from better_auth import auth  # This would be the Node.js handler

app = FastAPI()

@app.api_route("/auth/{path:path}", methods=["GET", "POST", "PUT", "DELETE"])
async def handle_auth(request: Request, path: str):
    # Implementation to delegate to Better Auth
    pass
```

2. Set up database tables:
```bash
npx @better-auth/cli migrate
```

### Frontend Configuration

1. Create auth client in Docusaurus:
```javascript
// frontend/src/auth.js
import { createAuthClient } from "better-auth/react";

export const authClient = createAuthClient({
  fetchOptions: {
    baseUrl: "http://localhost:8000", // Your FastAPI backend URL
  },
});
```

2. Add signup/signin pages:
```javascript
// frontend/src/pages/signup.js
import { authClient } from "../auth";

export default function SignupPage() {
  // Implementation using authClient
}
```

## Environment Setup

1. Create `.env` file in backend:
```
DATABASE_URL=your_neon_postgres_connection_string
BETTER_AUTH_SECRET=generate_a_strong_secret
BETTER_AUTH_URL=http://localhost:8000
BETTER_AUTH_TRUSTED_ORIGINS=http://localhost:3000,http://localhost:8000
```

2. For Neon Postgres, the DATABASE_URL format is:
```
postgresql://<user>:<password>@<host>:<port>/<database>?sslmode=require
```

## Running the Application

### Development

1. Start the backend:
```bash
cd backend
uvicorn main:app --reload --port 8000
```

2. Start the frontend:
```bash
cd frontend
npm run start
```

## API Endpoints

### Authentication Endpoints
- `POST /auth/signin` - User sign in
- `POST /auth/signup` - User registration
- `POST /auth/signout` - User sign out
- `GET /auth/session` - Get current session

### User Profile Endpoints
- `POST /api/user-profile` - Create/update user profile with consent
- `GET /api/user-profile` - Get user profile (authenticated users only)

### RAG Endpoints (Unchanged)
- `POST /api/query` - Query the RAG system (accessible to all)
- `POST /api/select` - Select relevant documents (accessible to all)

## User Flow

1. **Anonymous Access**: Users can access RAG features without authentication
2. **Registration**: Users can sign up and provide background information with explicit consent
3. **Authentication**: Users can sign in to access personalized features
4. **Profile Management**: Authenticated users can update their background information

## Testing

1. Verify authentication works:
```bash
curl -X POST http://localhost:8000/auth/signup \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com", "password":"password123"}'
```

2. Verify RAG endpoints remain accessible:
```bash
curl -X POST http://localhost:8000/api/query \
  -H "Content-Type: application/json" \
  -d '{"query":"test query"}'
```

## Troubleshooting

- If authentication endpoints return 404, verify the catch-all route is properly configured
- If database migrations fail, ensure your DATABASE_URL is correct
- If sessions aren't persisting, check that cookies are configured properly
- If RAG endpoints become blocked, verify that authentication middleware doesn't intercept them