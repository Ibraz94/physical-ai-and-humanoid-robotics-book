# Clarifications: Better Auth Integration

## Session 2025-12-19

- Q: Which existing backend infrastructure needs to be adapted for Better Auth integration? → A: The existing API key validation middleware in backend/app/middleware.py needs to be updated to allow anonymous access to RAG endpoints (POST /query, POST /select) while still protecting other endpoints
- Q: What frontend pages already exist vs. need to be created? → A: The Docusaurus frontend exists with index.tsx, but auth-specific pages (signup, signin) need to be created in the src/pages/ directory
- Q: How should the existing User model be handled with Better Auth? → A: The existing User model in backend/app/models/user.py should be kept but linked to Better Auth's user management, with profile data stored in the new user_profiles table
- Q: What's the current state of RAG endpoints that need to remain accessible? → A: RAG endpoints (query.py, select.py) already exist but are currently blocked by API key validation middleware that needs modification
- Q: How should session management coexist with existing security measures? → A: Better Auth sessions will work alongside existing API key system, with middleware updated to allow anonymous RAG access while maintaining security for other endpoints

## Applied Updates

### Functional Requirements Updated:
- Modified requirement to update existing API key validation middleware to allow anonymous access to RAG endpoints
- Added requirement to create signup and signin pages for Docusaurus frontend
- Clarified that existing User model should be enhanced rather than replaced

### Data Model Updated:
- Added clarification that the existing User model will be used alongside Better Auth's user management
- Specified that user_profiles table will link to Better Auth users via foreign key relationship

### User Stories Enhanced:
- User Story 1: Focus shifted to modifying existing middleware rather than creating new endpoints
- User Story 2: Emphasis on creating frontend pages and linking to existing backend infrastructure
- User Story 3: Integration with existing security framework rather than replacing it

## Outstanding Considerations:
- The existing API key system may need adjustment to work harmoniously with Better Auth sessions
- CORS configuration should align with both existing and new authentication requirements
- Database migration needs to accommodate both Better Auth tables and application-specific user_profiles table