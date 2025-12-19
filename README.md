# Physical AI & Humanoid Robotics Book

A comprehensive technical book about building physical AI systems and humanoid robots, featuring an AI-powered chatbot assistant.

## Overview

This repository contains the source code and content for the "Physical AI & Humanoid Robotics" book. The project uses Docusaurus v3 for the frontend, FastAPI for the backend, and Better Auth for authentication. It includes an intelligent RAG-based chatbot that helps users learn about robotics and physical AI.

## Features

- 📚 **Interactive Learning**: Comprehensive modules on physical AI and robotics
- 🤖 **AI Chatbot Assistant**: RAG-based chatbot powered by Gemini and Cohere
- 🔐 **User Authentication**: Secure sign-up/sign-in with Better Auth
- 🎨 **Modern UI**: Futuristic design with dark/light mode support
- 📱 **Responsive Design**: Works seamlessly on desktop and mobile
- 🔍 **Vector Search**: Qdrant-powered semantic search for accurate answers

## Architecture

The project uses a three-server architecture:

1. **Frontend (Port 3000)**: Docusaurus + React
   - Authentication pages (sign in/sign up)
   - Interactive chatbot interface
   - Book content and navigation

2. **Backend (Port 8000)**: FastAPI + Python
   - RAG chatbot endpoints
   - Proxies auth requests to Better Auth
   - Vector database integration (Qdrant)

3. **Auth Server (Port 8001)**: Better Auth + Node.js
   - Handles authentication logic
   - Session management
   - PostgreSQL database (Neon)

## Quickstart

### Prerequisites
- Node.js 20+
- Python 3.8+
- PostgreSQL database (Neon recommended)

### Installation

1. **Install Frontend Dependencies**
```bash
npm install
```

2. **Install Backend Dependencies**
```bash
cd backend
pip install -r requirements.txt
npm install
```

3. **Configure Environment**
```bash
cd backend
cp .env.example .env
# Edit .env with your database credentials and API keys
```

4. **Run Database Migrations**
```bash
cd backend
npm run migrate
```

### Running the Application

You need to start all three servers. See [START_SERVERS.md](START_SERVERS.md) for detailed instructions.

**Quick Start:**

```bash
# Terminal 1: Better Auth Server
cd backend
npm run dev

# Terminal 2: FastAPI Backend
cd backend
.venv\Scripts\activate  # Windows
# or: source .venv/bin/activate  # Mac/Linux
uvicorn app.main:app --reload --port 8000

# Terminal 3: Frontend
npm start
```

Then visit: http://localhost:3000/physical-ai-and-humanoid-robotics-book/

### Local Development

```bash
npm start
```
Opens http://localhost:3000/physical-ai-and-humanoid-robotics-book/

### Build & Validation

```bash
npm run build
```
Checks for broken links and generates static artifacts in `build/`.

## Project Structure

```
├── docs/                    # Book chapters (Markdown/MDX)
├── src/
│   ├── components/
│   │   ├── auth/           # Authentication components
│   │   ├── chat/           # Chatbot components
│   │   └── homepage/       # Homepage components
│   ├── pages/              # Custom pages (signin, signup)
│   ├── theme/              # Swizzled Docusaurus components
│   └── css/                # Global styles
├── backend/
│   ├── app/                # FastAPI application
│   │   ├── api/           # API endpoints
│   │   ├── services/      # Business logic
│   │   └── middleware.py  # Security middleware
│   ├── auth-server.ts     # Better Auth server
│   ├── auth.config.ts     # Auth configuration
│   └── .env               # Environment variables
├── static/                 # Static assets (images, diagrams)
├── specs/                  # Project specifications
└── START_SERVERS.md       # Detailed server setup guide

## Authentication

The application uses Better Auth for secure user authentication:

- **Sign Up**: Create an account with email/password
- **Sign In**: Access your account
- **Session Management**: 7-day sessions with automatic refresh
- **Protected Features**: Chatbot requires authentication

### User Flow

1. Visit the site (unauthenticated)
2. Sign up with email and password
3. Redirected to homepage
4. Access chatbot and other features
5. Sign out when done

## Chatbot

The AI chatbot assistant helps users learn about physical AI and robotics:

- **RAG-based**: Uses Retrieval Augmented Generation
- **Vector Search**: Qdrant for semantic search
- **LLM**: Powered by Google Gemini
- **Embeddings**: Cohere for text embeddings
- **Context-Aware**: Understands book content
- **Authentication Required**: Must sign in to use

## Testing

See [START_SERVERS.md](START_SERVERS.md) for comprehensive testing instructions including:
- Authentication flow testing
- Chatbot access testing
- Dark/light mode testing
- Navbar integration testing

## Troubleshooting

Common issues and solutions are documented in [START_SERVERS.md](START_SERVERS.md).

Quick checks:
- Verify all three servers are running
- Check browser console for errors (F12)
- Verify database connection in `backend/.env`
- Clear browser cookies/cache if session issues occur

## Environment Variables

Required environment variables in `backend/.env`:

```env
# Database
DATABASE_URL="postgresql://..."

# Better Auth
BETTER_AUTH_SECRET="your-secret-key"
BETTER_AUTH_URL="http://localhost:8001"
BETTER_AUTH_TRUSTED_ORIGINS="http://localhost:3000,http://localhost:8000"

# Qdrant Vector Database
QDRANT_URL="https://..."
QDRANT_API_KEY="..."

# Cohere (Embeddings)
COHERE_API_KEY="..."

# Google Gemini (LLM)
GEMINI_API_KEY="..."
GEMINI_MODEL="gemini-2.5-flash"

# Backend Configuration
BACKEND_API_URL="http://localhost:8000"
BOOK_DOMAIN="http://localhost:3000"
```

## Development Workflow

1. **Make Changes**: Edit files in `src/`, `docs/`, or `backend/`
2. **Test Locally**: All servers support hot reload
3. **Check Diagnostics**: Use browser DevTools and server logs
4. **Build**: Run `npm run build` to verify
5. **Commit**: Push changes to GitHub
6. **Deploy**: Automatic deployment via GitHub Actions

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly (see START_SERVERS.md)
5. Submit a pull request

## Deployment

This project is automatically deployed to GitHub Pages via GitHub Actions on every push to the `main` branch.

Production deployment requires:
- Setting up environment variables in GitHub Secrets
- Configuring production database
- Updating BETTER_AUTH_URL and BETTER_AUTH_TRUSTED_ORIGINS
- Enabling email verification in auth.config.ts

## Documentation

- [START_SERVERS.md](START_SERVERS.md) - Comprehensive server setup and testing guide
- [docs/](docs/) - Book content and learning modules
- [specs/](specs/) - Project specifications and architecture

## Tech Stack

**Frontend:**
- Docusaurus 3.9.2
- React 19
- Better Auth React Client
- CSS Modules

**Backend:**
- FastAPI (Python)
- Better Auth (Node.js/TypeScript)
- Qdrant (Vector Database)
- PostgreSQL (Neon)
- Cohere (Embeddings)
- Google Gemini (LLM)

## License

MIT