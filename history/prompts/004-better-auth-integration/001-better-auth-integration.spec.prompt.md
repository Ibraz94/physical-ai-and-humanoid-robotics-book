---
id: "001"
title: "Better Auth Integration Specification"
stage: "spec"
date: "2025-12-19"
surface: "agent"
model: "Claude Sonnet 4.5"
feature: "better-auth-integration"
branch: "004-better-auth-integration"
user: "user"
command: "/sp.specify spec 004 Integrate Better Auth into an existing project where: Frontend is Docusaurus (React), Backend is FastAPI (Python), Database is Neon Serverless Postgres, Authentication is optional, Core RAG chatbot must remain usable without login"
labels: ["auth", "better-auth", "specification", "docusaurus", "fastapi"]
links:
  spec: "null"
  ticket: "null"
  adr: "null"
  pr: "null"
files:
  - "specs/004-better-auth-integration/spec.md"
  - "specs/004-better-auth-integration/checklists/requirements.md"
tests: []
---

## Prompt Text

```
spec 004 Integrate Better Auth into an existing project where:

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

RAG endpoints unaffected
```

## Response Text

Created comprehensive specification for Better Auth integration with Docusaurus frontend and FastAPI backend, including user scenarios, functional requirements, and success criteria while maintaining RAG chatbot accessibility for anonymous users.

## Outcome

Specification successfully created at specs/004-better-auth-integration/spec.md with all requirements addressed. The spec includes user stories for anonymous RAG access, user registration with background information, and authentication management. All functional requirements ensure RAG endpoints remain accessible without authentication while supporting user profiles with explicit consent for data storage.