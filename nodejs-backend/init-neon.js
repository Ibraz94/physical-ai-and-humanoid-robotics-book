/**
 * Initialize Neon configuration BEFORE any other imports
 * This must be imported first in auth-server.ts
 */

import { neonConfig } from '@neondatabase/serverless';
import ws from 'ws';
import crypto from 'crypto';

// Configure Neon to use ws library instead of native WebSocket
// This is required for Node.js environments
neonConfig.webSocketConstructor = ws;

// Make crypto available globally for Better Auth
if (typeof global !== 'undefined') {
  global.crypto = crypto;
}

console.log('✅ Neon configured with ws library');
console.log('✅ Crypto module configured');
