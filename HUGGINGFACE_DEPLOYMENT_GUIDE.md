# Hugging Face Spaces Deployment Guide

## Overview
You need to deploy TWO separate Spaces:
1. **Python Backend Space** - FastAPI backend
2. **Node.js Backend Space** - Better Auth authentication server

---

## Part 1: Deploy Python Backend

### Step 1: Create Python Backend Space

1. Go to https://huggingface.co/spaces
2. Click **"Create new Space"**
3. Fill in the details:
   - **Space name**: `rag-chatbot-python-backend` (or your preferred name)
   - **License**: Choose appropriate license
   - **Select SDK**: Choose **Docker**
   - **Space hardware**: CPU basic (free) or upgrade if needed
   - **Visibility**: Public or Private
4. Click **"Create Space"**

### Step 2: Prepare Python Backend Files

Create a new folder locally for the Python backend Space:

```bash
mkdir python-backend-space
cd python-backend-space
```

Copy these files from your `backend/` folder:
- `Dockerfile.python` → rename to `Dockerfile`
- `app/` folder (entire directory)
- `ingestion/` folder (entire directory)
- `pyproject.toml`
- `uv.lock`
- `README.md`

### Step 3: Create README.md with Metadata

Update the `README.md` to include Hugging Face metadata at the top:

```markdown
---
title: RAG Chatbot Python Backend
emoji: 🤖
colorFrom: blue
colorTo: green
sdk: docker
app_port: 7860
---

# RAG Chatbot Python Backend

FastAPI backend for RAG chatbot with OpenAI Agents SDK and Gemini.

## Environment Variables

Configure these in Space Settings:
- DATABASE_URL
- QDRANT_URL
- QDRANT_API_KEY
- COHERE_API_KEY
- GEMINI_API_KEY
- GEMINI_MODEL
- BOOK_DOMAIN
- BETTER_AUTH_URL
```

### Step 4: Update Dockerfile

Make sure your `Dockerfile` (renamed from Dockerfile.python) has the correct paths:

```dockerfile
FROM python:3.11-slim as builder

WORKDIR /app

# Install build dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy project files
COPY pyproject.toml ./
COPY uv.lock ./

# Install uv and dependencies
RUN pip install uv && uv pip install --system --requirement uv.lock

FROM python:3.11-slim

# Create non-root user for security
RUN groupadd -r appuser && useradd -r -g appuser appuser

WORKDIR /app

# Install runtime dependencies
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy installed Python packages from builder stage
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages

# Copy application code
COPY app/ ./app/
COPY ingestion/ ./ingestion/

# Change ownership to non-root user
RUN chown -R appuser:appuser /app
USER appuser

EXPOSE 7860

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:7860/health || exit 1

# Run the application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "7860", "--workers", "2"]
```

### Step 5: Push to Python Backend Space

Initialize git and push:

```bash
git init
git add .
git commit -m "Initial Python backend deployment"
git remote add space https://huggingface.co/spaces/YOUR_USERNAME/rag-chatbot-python-backend
git push --force space main
```

### Step 6: Configure Environment Variables

1. Go to your Space settings: `https://huggingface.co/spaces/YOUR_USERNAME/rag-chatbot-python-backend/settings`
2. Scroll to **"Repository secrets"**
3. Add these secrets:
   - `DATABASE_URL`: Your Neon Postgres connection string
   - `QDRANT_URL`: Your Qdrant instance URL
   - `QDRANT_API_KEY`: Your Qdrant API key
   - `COHERE_API_KEY`: Your Cohere API key
   - `GEMINI_API_KEY`: Your Google Gemini API key
   - `GEMINI_MODEL`: `gemini-pro`
   - `BOOK_DOMAIN`: Your frontend URL (will add later)
   - `BETTER_AUTH_URL`: Your Node.js backend Space URL (will add after Part 2)

4. Click **"Save"** after adding each secret

---

## Part 2: Deploy Node.js Backend

### Step 1: Create Node.js Backend Space

1. Go to https://huggingface.co/spaces
2. Click **"Create new Space"**
3. Fill in the details:
   - **Space name**: `rag-chatbot-nodejs-backend` (or your preferred name)
   - **License**: Choose appropriate license
   - **Select SDK**: Choose **Docker**
   - **Space hardware**: CPU basic (free) or upgrade if needed
   - **Visibility**: Public or Private
4. Click **"Create Space"**

### Step 2: Prepare Node.js Backend Files

Create a new folder locally for the Node.js backend Space:

```bash
mkdir nodejs-backend-space
cd nodejs-backend-space
```

Copy these files from your `nodejs-backend/` folder:
- `Dockerfile` (already exists)
- `auth-server.ts`
- `auth.config.ts`
- `tsconfig.json`
- `package.json`
- `package-lock.json`
- `README.md`

### Step 3: Update README.md with Metadata

Update the `README.md`:

```markdown
---
title: RAG Chatbot Auth Server
emoji: 🔐
colorFrom: blue
colorTo: purple
sdk: docker
app_port: 7860
---

# RAG Chatbot Authentication Server

Node.js authentication backend with Better Auth and Neon Serverless Postgres.

## Environment Variables

Configure these in Space Settings:
- DATABASE_URL
- BETTER_AUTH_SECRET
- BETTER_AUTH_URL
- BETTER_AUTH_TRUSTED_ORIGINS
```

### Step 4: Verify Dockerfile

Your `Dockerfile` should look like this:

```dockerfile
FROM node:18-alpine

WORKDIR /app

# Install curl for health checks
RUN apk add --no-cache curl

# Copy package files
COPY package.json .
COPY package-lock.json .

# Install dependencies
RUN npm ci --only=production

# Install tsx globally for running TypeScript
RUN npm install -g tsx

# Copy application code
COPY auth-server.ts .
COPY auth.config.ts .
COPY tsconfig.json .

# Set environment variable for port
ENV AUTH_PORT=7860

EXPOSE 7860

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:7860/health || exit 1

# Run the application
CMD ["npm", "start"]
```

### Step 5: Push to Node.js Backend Space

Initialize git and push:

```bash
git init
git add .
git commit -m "Initial Node.js backend deployment"
git remote add space https://huggingface.co/spaces/YOUR_USERNAME/rag-chatbot-nodejs-backend
git push --force space main
```

### Step 6: Configure Environment Variables

1. Go to your Space settings: `https://huggingface.co/spaces/YOUR_USERNAME/rag-chatbot-nodejs-backend/settings`
2. Scroll to **"Repository secrets"**
3. Add these secrets:
   - `DATABASE_URL`: Your Neon Postgres connection string (same as Python backend)
   - `BETTER_AUTH_SECRET`: Generate a secure random string (e.g., use `openssl rand -hex 32`)
   - `BETTER_AUTH_URL`: `https://YOUR_USERNAME-rag-chatbot-nodejs-backend.hf.space`
   - `BETTER_AUTH_TRUSTED_ORIGINS`: Your frontend URL and Python backend URL (comma-separated)

4. Click **"Save"** after adding each secret

---

## Part 3: Update Cross-References

### Update Python Backend Environment Variables

Go back to your Python backend Space settings and update:
- `BETTER_AUTH_URL`: `https://YOUR_USERNAME-rag-chatbot-nodejs-backend.hf.space`
- `BOOK_DOMAIN`: Your frontend URL (if deployed)

### Update Node.js Backend Environment Variables

Update:
- `BETTER_AUTH_TRUSTED_ORIGINS`: Add both frontend and Python backend URLs

---

## Part 4: Verify Deployments

### Check Python Backend

1. Go to `https://YOUR_USERNAME-rag-chatbot-python-backend.hf.space`
2. Check the logs for any errors
3. Test the health endpoint: `https://YOUR_USERNAME-rag-chatbot-python-backend.hf.space/health`

### Check Node.js Backend

1. Go to `https://YOUR_USERNAME-rag-chatbot-nodejs-backend.hf.space`
2. Check the logs for any errors
3. Test the health endpoint: `https://YOUR_USERNAME-rag-chatbot-nodejs-backend.hf.space/health`

---

## Troubleshooting

### Build Failures

**Python Backend:**
- Check that `pyproject.toml` and `uv.lock` are in the root
- Verify all Python dependencies are listed
- Check logs for missing system packages

**Node.js Backend:**
- Ensure `package.json` and `package-lock.json` are present
- Verify tsx is installed globally in Dockerfile
- Check for TypeScript compilation errors

### Runtime Errors

**Database Connection:**
- Verify `DATABASE_URL` is correct
- Check if Neon database is accessible from Hugging Face
- Ensure database has proper tables/schema

**CORS Issues:**
- Update `BETTER_AUTH_TRUSTED_ORIGINS` with correct URLs
- Add frontend URL to `BOOK_DOMAIN`

**Port Issues:**
- Both backends must run on port 7860 (Hugging Face requirement)
- Check `app_port: 7860` in README.md metadata

---

## Important Notes

1. **Free Tier Limitations**: Hugging Face free tier may have CPU/memory limits. Upgrade if needed.

2. **Cold Starts**: Spaces may sleep after inactivity. First request might be slow.

3. **Environment Variables**: Never commit secrets to git. Always use Space settings.

4. **HTTPS**: All Hugging Face Spaces URLs use HTTPS automatically.

5. **Custom Domains**: You can add custom domains in Space settings (paid feature).

6. **Logs**: Monitor logs in the Space UI for debugging.

7. **Updates**: Push to the Space repository to trigger rebuilds.

---

## Quick Commands Reference

```bash
# Clone your Space
git clone https://huggingface.co/spaces/YOUR_USERNAME/SPACE_NAME

# Make changes and push
git add .
git commit -m "Update message"
git push

# Force push (if needed)
git push --force
```

---

## Next Steps

After both backends are deployed:
1. Update your frontend to use the new backend URLs
2. Test authentication flow
3. Test RAG query functionality
4. Monitor logs for any issues
5. Consider upgrading hardware if performance is slow
