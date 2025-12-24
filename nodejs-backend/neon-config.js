/**
 * Neon Configuration for Hugging Face Spaces
 * 
 * This file configures Neon to use HTTP fetch instead of WebSockets
 * which are not available in Hugging Face Spaces environment.
 */

import { neonConfig } from '@neondatabase/serverless';

// Disable WebSocket and use HTTP fetch instead
// This is required for environments without WebSocket support
neonConfig.fetchConnectionCache = true;
neonConfig.useSecureWebSocket = false;

// Set WebSocket constructor to undefined to force HTTP mode
if (typeof WebSocket === 'undefined' || process.env.NEON_USE_HTTP === 'true') {
  neonConfig.webSocketConstructor = undefined;
}

console.log('Neon configured to use HTTP fetch (WebSocket disabled)');

export default neonConfig;
