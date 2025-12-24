/**
 * WebSocket Polyfill for Neon
 * 
 * This prevents Neon from trying to use WebSocket
 * by providing a dummy WebSocket that immediately fails,
 * forcing Neon to fall back to HTTP fetch
 */

// Set WebSocket to undefined globally to force HTTP mode
if (typeof global !== 'undefined') {
  global.WebSocket = undefined;
}

console.log('✅ WebSocket disabled - Neon will use HTTP fetch');
