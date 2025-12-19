# Feature Specification: Better Auth Integration

**Feature Branch**: `004-better-auth-integration`
**Created**: 2025-12-19
**Status**: Draft
**Input**: User description: "spec 004 Integrate Better Auth into an existing project where:

Frontend is Docusaurus (React)

Backend is FastAPI (Python)

Database is Neon Serverless Postgres

Authentication is optional

Core RAG chatbot must remain usable without login

Global Constraints (Non-Negotiable)

Better Auth MCP Server MUST be used for all auth-related APIs and flows

Context7 MCP Server MUST be used for:

FastAPI integration patterns

Environment variable configuration

No undocumented or guessed APIs

No auth logic may block:

POST /query

POST /select

No PII storage without explicit user consent

Frontend and backend must run without runtime errors

Step-by-Step Execution Plan
Step 1 — Documentation Verification (MANDATORY FIRST STEP)

Use Better Auth MCP Server to retrieve:

Backend (FastAPI) integration documentation

React client usage (non-Next.js)

Session and cookie handling

Use Context7 MCP Server to verify:

FastAPI middleware patterns

Secure environment variable usage

Do NOT write code until documentation is verified

Output: Confirmed, MCP-verified API references

Step 2 — Backend: Initialize Better Auth (FastAPI)

Add Better Auth to the FastAPI backend

Configure:

Email/password authentication (minimum)

Session handling via cookies

Connect Better Auth to Neon Serverless Postgres

Mount auth routes (example paths, follow docs exactly):

/auth/signup
/auth/signin
/auth/signout
/auth/session


Keep auth routes fully isolated from RAG routes

Rule: RAG endpoints must work with or without auth

Step 3 — Database: Neon Postgres Schema

Allow Better Auth to manage its own tables:

users

sessions

credentials

Create an application-owned table:

user_profiles
- user_id (FK to auth users)
- software_background
- hardware_background
- consent_given
- created_at


Ensure no background data is stored without consent

Step 4 — Frontend: Signup & Signin (Docusaurus React)

Create React pages/components:

/signup

/signin

Use Better Auth's React client (non-Next.js)

During signup:

Ask for software background

Ask for hardware background

Require explicit consent checkbox

On successful signup:

Store background data via backend API

On signin:

Restore session using cookies

Rule: Chatbot must remain usable without login

Step 5 — Session Handling in FastAPI

Add Better Auth session validation middleware

For every request:

If session exists → attach user_id to request context

If no session → continue anonymously

Never reject requests to:

POST /query
POST /select

Step 6 — Ensure RAG Compatibility

Do NOT modify:

Retrieval logic

Grounding rules

Agent behavior

Auth context may be:

Passed as optional metadata

Used later for personalization only

RAG answers must remain:

Context-grounded

Deterministic

Auth-independent

Step 7 — Validation (Required)
Frontend Validation

Signup works

Signin works

Auth errors handled gracefully

Chatbot works anonymously

No console or runtime errors

Backend Validation

FastAPI starts without errors

Auth routes work

Sessions validate correctly

RAG endpoints unaffected"

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Anonymous RAG Chatbot Access (Priority: P1)

A visitor can use the RAG chatbot without creating an account or logging in. They can ask questions and receive responses from the system without any authentication requirements.

**Why this priority**: This maintains the core functionality that allows users to immediately access the chatbot, which is essential for user experience and adoption.

**Independent Test**: Can be fully tested by accessing the chatbot interface and submitting queries without authentication, delivering immediate value to users who want to explore the system.

**Acceptance Scenarios**:

1. **Given** a user visits the site, **When** they access the RAG chatbot without logging in, **Then** they can submit queries and receive responses
2. **Given** a user is not authenticated, **When** they make POST /query requests, **Then** the system processes the request without requiring authentication

---

### User Story 2 - User Registration with Background Information (Priority: P2)

A visitor can create an account by providing email, password, software background, hardware background, and explicit consent to store their personal information.

**Why this priority**: This enables user personalization and data collection while maintaining privacy compliance through explicit consent.

**Independent Test**: Can be fully tested by completing the signup flow and verifying that user data is stored only after explicit consent, delivering value through account creation and profile management.

**Acceptance Scenarios**:

1. **Given** a visitor accesses the signup page, **When** they provide valid credentials and background information with consent, **Then** their account is created and profile is saved
2. **Given** a visitor attempts to sign up without providing consent, **When** they submit the form, **Then** the system prevents account creation and shows an error message
3. **Given** a visitor provides invalid credentials, **When** they submit the form, **Then** the system shows appropriate validation errors

---

### User Story 3 - User Authentication and Session Management (Priority: P3)

A registered user can sign in to their account, maintain a session, and sign out when finished, with proper session management handled via cookies.

**Why this priority**: This enables personalized experiences while maintaining security and proper user session lifecycle.

**Independent Test**: Can be fully tested by signing in, using the system with an active session, and signing out, delivering value through secure access to user-specific features.

**Acceptance Scenarios**:

1. **Given** a user has a valid account, **When** they provide correct credentials on the signin page, **Then** they are authenticated and receive a valid session
2. **Given** a user is authenticated, **When** they access protected features, **Then** the system recognizes their session and grants appropriate access
3. **Given** a user is signed in, **When** they sign out, **Then** their session is terminated and they return to anonymous access

---

### Edge Cases

- What happens when a user tries to access the chatbot during authentication token refresh?
- How does the system handle expired sessions during long-running RAG queries?
- What occurs when the database is temporarily unavailable during authentication?
- How does the system behave when consent is revoked by a user?
- What happens if a user attempts to sign up with an email that already exists?

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST support email/password authentication using Better Auth framework
- **FR-002**: System MUST maintain user sessions via cookies with proper security settings
- **FR-003**: System MUST connect Better Auth to Neon Serverless Postgres for user data storage
- **FR-004**: System MUST provide standard auth routes: /auth/signup, /auth/signin, /auth/signout, /auth/session
- **FR-005**: System MUST allow anonymous access to RAG endpoints (POST /query, POST /select) without authentication
- **FR-006**: System MUST collect software background, hardware background, and explicit consent during user registration
- **FR-007**: System MUST store user profile data only after explicit consent is provided
- **FR-008**: System MUST validate user sessions for authenticated requests while allowing anonymous access for RAG endpoints
- **FR-009**: System MUST attach user_id to request context when a valid session exists
- **FR-010**: System MUST continue processing RAG requests anonymously when no session exists
- **FR-011**: System MUST provide signup and signin pages/components for Docusaurus React frontend
- **FR-012**: System MUST handle authentication errors gracefully without disrupting the RAG chatbot functionality
- **FR-013**: System MUST maintain RAG chatbot functionality identical for both authenticated and anonymous users
- **FR-014**: System MUST store user background information in a user_profiles table linked to Better Auth users
- **FR-015**: System MUST ensure no PII is stored without explicit user consent

### Key Entities *(include if feature involves data)*

- **User**: Represents a registered user with email/password credentials managed by Better Auth
- **UserProfile**: Contains user-specific information including software background, hardware background, and consent status, linked to the User entity
- **Session**: Represents an authenticated user session managed by Better Auth with proper cookie handling

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Users can access the RAG chatbot without authentication and submit queries with 99% success rate
- **SC-002**: User registration process completes successfully within 2 minutes when all required information is provided
- **SC-003**: User authentication (signin/signout) processes complete within 5 seconds with 99% success rate
- **SC-004**: 95% of users successfully complete registration when they choose to create an account
- **SC-005**: RAG query performance remains unchanged (within 10%) for both authenticated and anonymous users
- **SC-006**: System handles authentication errors gracefully without affecting RAG chatbot functionality
- **SC-007**: All user profile data is stored only after explicit consent, with 100% compliance rate
- **SC-008**: Frontend and backend applications run without runtime errors related to authentication