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
    "http://localhost:8000", // FastAPI backend
    process.env.BOOK_DOMAIN || "",
  ],
});

// Export the auth instance for use in the application
export default auth;