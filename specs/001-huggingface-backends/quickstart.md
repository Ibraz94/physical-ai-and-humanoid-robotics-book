# Quickstart: Hugging Face Spaces Backend Deployment

## Overview
This guide provides instructions for deploying two independent backend services (Python and Node.js) on Hugging Face Spaces using Docker SDK.

## Prerequisites
- Git
- Docker (for local testing)
- Hugging Face account
- Basic knowledge of Docker and containerization

## Repository Structure
```
project-root/
├── python-backend/
│   ├── app.py
│   ├── requirements.txt
│   ├── Dockerfile
│   └── README.md
├── nodejs-backend/
│   ├── server.js
│   ├── package.json
│   ├── Dockerfile
│   └── README.md
└── docker/
    ├── python/
    │   └── Dockerfile
    └── nodejs/
        └── Dockerfile
```

## Python Backend Setup

1. Navigate to the python-backend directory:
```bash
cd python-backend
```

2. Create your Python application (app.py):
```python
import os
from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello():
    return {"message": "Python backend running on Hugging Face Spaces"}

@app.route('/health')
def health():
    return {"status": "healthy"}

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 7860))
    app.run(host='0.0.0.0', port=port)
```

3. Define dependencies in requirements.txt:
```
Flask==2.3.3
gunicorn==21.2.0
python-dotenv==1.0.0
```

4. Create Dockerfile:
```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 7860

HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:7860/health || exit 1

CMD ["gunicorn", "--bind", "0.0.0.0:7860", "--workers", "2", "app:app"]
```

5. Create Hugging Face Spaces compliant README.md:
```markdown
---
sdk: docker
app_port: 7860
---
# Python Backend

This is a Python backend service deployed on Hugging Face Spaces.
```

## Node.js Backend Setup

1. Navigate to the nodejs-backend directory:
```bash
cd nodejs-backend
```

2. Create your Node.js application (server.js):
```javascript
const express = require('express');
const app = express();
const port = process.env.PORT || 7860;

app.get('/', (req, res) => {
  res.json({ message: "Node.js backend running on Hugging Face Spaces" });
});

app.get('/health', (req, res) => {
  res.json({ status: 'healthy' });
});

app.listen(port, '0.0.0.0', () => {
  console.log(`Node.js server running on port ${port}`);
});
```

3. Define dependencies in package.json:
```json
{
  "name": "nodejs-backend",
  "version": "1.0.0",
  "main": "server.js",
  "dependencies": {
    "express": "^4.18.2"
  },
  "scripts": {
    "start": "node server.js"
  }
}
```

4. Create Dockerfile:
```dockerfile
FROM node:18-alpine

WORKDIR /app

COPY package*.json ./
RUN npm install --production

COPY . .

EXPOSE 7860

HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
  CMD node healthcheck.js || exit 1

CMD ["node", "server.js"]
```

5. Create Hugging Face Spaces compliant README.md:
```markdown
---
sdk: docker
app_port: 7860
---
# Node.js Backend

This is a Node.js backend service deployed on Hugging Face Spaces.
```

## Deployment to Hugging Face Spaces

1. Create a new Space on Hugging Face
2. Choose "Docker" as the SDK
3. Point the Space to your repository containing the backend
4. The Space will automatically build and deploy using the Dockerfile

## Environment Variables

Both backends support environment variable configuration:

Python (.env.example):
```
PORT=7860
DEBUG=False
API_KEY=your_api_key_here
```

Node.js (.env.example):
```
PORT=7860
NODE_ENV=production
API_KEY=your_api_key_here
```

## Health Checks

Both backends include health check endpoints at `/health` that return a 200 status when the service is operational.