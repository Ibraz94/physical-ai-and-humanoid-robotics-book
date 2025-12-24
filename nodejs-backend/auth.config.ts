/**
 * Better Auth Configuration
 *
 * This configuration sets up Better Auth with Neon Postgres database adapter
 * and defines the authentication flows for the application.
 */

import { betterAuth } from "better-auth";
import { Pool } from "@neondatabase/serverless";

// Initialize Neon database connection pool
const pool = new Pool({ connectionString: process.env.DATABASE_URL });

// Create the Better Auth instance with configuration
export const auth = betterAuth({
  database: pool,

  // Email and password authentication configuration
  emailAndPassword: {
    enabled: true,
    requireEmailVerification: false, // Set to true in production for security
  },

  // Session configuration
  session: {
    expiresIn: 60 * 60 * 24 * 7, // 7 days in seconds
    updateAge: 60 * 60 * 24, // Update session age every 24 hours if active
  },

  // Advanced configuration
  advanced: {
    /**
     * Configure CORS settings
     */
    crossSubDomainCookies: {
      enabled: false,
    },
  },

  // Trust proxy for production deployments
  trustedOrigins: [
    "http://localhost:3000", // Docusaurus frontend in development
    "http://localhost:8000", // FastAPI backend in development
    "https://ibraz94.github.io", // GitHub Pages frontend (production)
    "https://ibraz-api-ai-book.hf.space", // Python backend on HF (production)
    "https://ibraz-auth-ai-book.hf.space", // Auth backend on HF (production)
    process.env.BOOK_DOMAIN || "",
    process.env.BETTER_AUTH_URL || "",
  ],
});

// Export the auth instance for use in the application
export default auth;