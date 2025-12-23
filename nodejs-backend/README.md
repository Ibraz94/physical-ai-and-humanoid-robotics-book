---
title: RAG Chatbot Auth Server
emoji: 🔐
colorFrom: blue
colorTo: purple
sdk: docker
app_port: 7860
---

# RAG Chatbot Authentication Server

This is the Node.js authentication backend for the RAG chatbot, built with Better Auth and Neon Serverless Postgres.

## Features

- Better Auth integration for secure authentication
- Session management
- User authentication endpoints
- Neon Serverless Postgres for user data storage

## Environment Variables

Required environment variables (set in Hugging Face Space settings):

```
DATABASE_URL=postgresql://username:password@host:port/database
BETTER_AUTH_SECRET=your-better-auth-secret
BETTER_AUTH_URL=https://your-space-url.hf.space
BETTER_AUTH_TRUSTED_ORIGINS=https://your-frontend-url.com
```

## Endpoints

- `POST /api/auth/sign-in`: User sign in
- `POST /api/auth/sign-up`: User registration
- `POST /api/auth/sign-out`: User sign out
- `GET /api/auth/session`: Get current session
- `GET /health`: Health check endpoint

## Local Development

```bash
# Install dependencies
npm install

# Run development server
npm run dev

# Run production server
npm start
```

## Docker Build

```bash
# Build the image
docker build -t rag-auth-server .

# Run the container
docker run -p 7860:7860 --env-file .env rag-auth-server
```

## Deployment to Hugging Face Spaces

1. Create a new Space with Docker SDK
2. Push this directory to the Space repository
3. Configure environment variables in Space settings
4. The Space will automatically build and deploy
