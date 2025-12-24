/**
 * Better Auth Server
 * Standalone Node.js server that handles authentication
 * Runs on port 8001 and is proxied by FastAPI on port 8000
 */

// CRITICAL: Initialize Neon configuration FIRST
import './init-neon.js';

import 'dotenv/config';
import { auth } from "./auth.config.js";
import { toNodeHandler } from "better-auth/node";
import { createServer } from "http";

const PORT = process.env.AUTH_PORT || 8001;

// Log configuration (without exposing sensitive data)
console.log('Environment check:');
console.log('- DATABASE_URL:', process.env.DATABASE_URL ? '✓ Set' : '✗ Not set');
console.log('- AUTH_PORT:', PORT);

// Create HTTP server with Better Auth handler
const handler = toNodeHandler(auth);

const server = createServer(async (req, res) => {
  console.log(`[${new Date().toISOString()}] ${req.method} ${req.url}`);
  
  // Health check endpoint
  if (req.url === '/health' && req.method === 'GET') {
    res.statusCode = 200;
    res.setHeader('Content-Type', 'application/json');
    res.end(JSON.stringify({ status: 'ok', service: 'auth-server' }));
    return;
  }
  
  try {
    await handler(req, res);
  } catch (error) {
    console.error('Error handling request:', error);
    res.statusCode = 500;
    res.end(JSON.stringify({ error: 'Internal server error' }));
  }
});

server.listen(PORT, () => {
  console.log(`✅ Better Auth server running on http://localhost:${PORT}`);
  console.log(`📍 Auth endpoints available at http://localhost:${PORT}/api/auth/*`);
  console.log(`\nAvailable endpoints:`);
  console.log(`  POST /api/auth/sign-up/email - Create account with email/password`);
  console.log(`  POST /api/auth/sign-in/email - Sign in with email/password`);
  console.log(`  POST /api/auth/sign-out - Sign out`);
  console.log(`  GET  /api/auth/session - Get current session`);
  console.log(`\nWaiting for requests...`);
});

// Handle graceful shutdown
process.on('SIGTERM', () => {
  console.log('SIGTERM signal received: closing HTTP server');
  server.close(() => {
    console.log('HTTP server closed');
    process.exit(0);
  });
});

process.on('SIGINT', () => {
  console.log('\nSIGINT signal received: closing HTTP server');
  server.close(() => {
    console.log('HTTP server closed');
    process.exit(0);
  });
});
