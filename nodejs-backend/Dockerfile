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

# Copy application code (excluding node_modules)
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