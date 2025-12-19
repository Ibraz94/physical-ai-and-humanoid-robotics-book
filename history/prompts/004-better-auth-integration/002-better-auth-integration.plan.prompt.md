---
id: "002"
title: "Better Auth Integration Plan"
stage: "plan"
date: "2025-12-19"
surface: "agent"
model: "Claude Sonnet 4.5"
feature: "better-auth-integration"
branch: "004-better-auth-integration"
user: "user"
command: "/sp.plan Plan the integration of Better Auth into an existing project where the frontend is built with Docusaurus (React) and the backend uses FastAPI (Python), with Neon Serverless Postgres as the database."
labels: ["auth", "better-auth", "plan", "fastapi", "docusaurus"]
links:
  spec: "specs/004-better-auth-integration/spec.md"
  ticket: "null"
  adr: "null"
  pr: "null"
files:
  - "specs/004-better-auth-integration/plan.md"
  - "specs/004-better-auth-integration/research.md"
  - "specs/004-better-auth-integration/data-model.md"
  - "specs/004-better-auth-integration/quickstart.md"
  - "specs/004-better-auth-integration/contracts/auth-api.yaml"
  - "specs/004-better-auth-integration/contracts/rag-api.yaml"
tests: []
---

## Prompt Text

```
Plan the integration of Better Auth into an existing project where the frontend is built with Docusaurus (React) and the backend uses FastAPI (Python), with Neon Serverless Postgres as the database. Authentication must be strictly optional and must never block or degrade the core RAG chatbot functionality. The plan must ensure a clean separation between authentication concerns and RAG logic, preserving anonymous access at all times while enabling authenticated users to benefit from session persistence and personalization in later phases.

Before any implementation is considered, the plan must require verification of all authentication-related APIs and flows using the Better Auth MCP Server, and verification of framework-level integration patterns and environment configuration using the Context7 MCP Server. No assumptions, undocumented APIs, or inferred behavior may be used. The plan must explicitly prevent authentication logic from interfering with existing chatbot endpoints such as POST /query and POST /select.

The plan should describe how Better Auth will be initialized in the FastAPI backend as a standalone authentication layer, with its own routes and session management, fully isolated from the RAG pipeline. It must account for Neon Postgres being used as the persistence layer for both Better Auth–managed identity data and application-owned user profile data, while maintaining a strict boundary between the two.

The plan must also cover how signup and signin flows will be implemented in the Docusaurus React frontend using Better Auth's React client, including the collection of user-provided software and hardware background information during signup. Explicit user consent must be planned as a prerequisite for storing any background data. The plan should ensure that session cookies are handled transparently by the browser and validated by the backend without requiring special handling in the chatbot UI.

Finally, the plan must include validation and documentation phases, ensuring that both frontend and bac
```

## Response Text

Completed comprehensive implementation plan for Better Auth integration with FastAPI backend and Docusaurus frontend. Key deliverables include:

1. **Research Summary**: Verified Better Auth doesn't have native FastAPI integration; created plan to use middleware layer approach
2. **Data Model**: Defined entities for User (managed by Better Auth), Session (managed by Better Auth), and UserProfile (application-owned)
3. **API Contracts**: Created OpenAPI specifications for auth endpoints and RAG endpoints (ensuring no auth requirement for RAG)
4. **Quickstart Guide**: Detailed setup instructions for both backend and frontend
5. **Implementation Plan**: Complete architecture with clear separation between auth and RAG layers

The plan ensures RAG endpoints (POST /query, POST /select) remain accessible to anonymous users while providing optional authentication with explicit consent for data storage.

## Outcome

Plan successfully completed with MCP server verification of Better Auth and FastAPI patterns. Created comprehensive documentation including data models, API contracts, and implementation guide. The plan maintains the critical requirement that authentication never blocks RAG functionality.