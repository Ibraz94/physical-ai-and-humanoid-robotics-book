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
COPY init-neon.js .
COPY auth-server.ts .
COPY auth.config.ts .
COPY tsconfig.json .

# Set environment variables
ENV AUTH_PORT=7860
ENV NEON_USE_HTTP=true

EXPOSE 7860

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:7860/health || exit 1

# Run the application
CMD ["npm", "start"]