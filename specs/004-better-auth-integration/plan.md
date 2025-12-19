# Implementation Plan: Better Auth Integration

**Branch**: `004-better-auth-integration` | **Date**: 2025-12-19 | **Spec**: specs/004-better-auth-integration/spec.md
**Input**: Feature specification from `/specs/004-better-auth-integration/spec.md`

**Note**: This template is filled in by the `/sp.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

Integrate Better Auth into existing Docusaurus (React) frontend and FastAPI (Python) backend with Neon Serverless Postgres. Based on MCP server research, since Better Auth does not have native FastAPI integration, we'll create a middleware layer to bridge Better Auth (Node.js) with FastAPI (Python). The implementation will provide optional email/password authentication with user profile collection (software/hardware background) requiring explicit consent. Critical requirement: maintain complete separation between authentication layer and RAG functionality, ensuring POST /query and POST /select endpoints remain accessible to anonymous users without performance degradation.

## Technical Context

**Language/Version**: Python 3.11 (FastAPI backend), JavaScript/TypeScript (Docusaurus frontend)
**Primary Dependencies**: FastAPI, Better Auth, Neon Postgres, Docusaurus, React
**Storage**: Neon Serverless Postgres database
**Testing**: pytest (backend), Jest/React Testing Library (frontend)
**Target Platform**: Web application (server-side rendering + client-side React)
**Project Type**: Web application (backend API + frontend UI)
**Performance Goals**: Maintain RAG query performance within 10% of baseline for both authenticated and anonymous users
**Constraints**: Authentication must never block RAG endpoints (POST /query, POST /select), PII stored only with explicit consent, maintain anonymous access to core functionality
**Scale/Scope**: Support optional authentication for users while preserving anonymous access for all RAG features

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

1. **I. Spec-First & Modular Design**: ✅ Plan follows spec-first approach, building on approved feature specification
2. **II. Educational Integrity**: ✅ Used MCP servers for authentication framework verification (Better Auth via Better Auth MCP, FastAPI patterns via Context7 MCP)
3. **III. Transparency and Traceability**: ✅ All auth-related APIs documented with source verification via MCP servers in research.md
4. **IV. Developer-Centric Documentation**: ✅ Plan includes clear API contracts (contracts/) and data models (data-model.md) for developer use
5. **V. Reproducible Content Pipeline**: ✅ Using Spec-Kit Plus and MCP-server integration as required
6. **VI. Web Ergonomics**: ✅ Authentication flows designed to not interfere with core RAG UX

**Post-Design Re-check**: All constitution checks continue to pass after Phase 1 design completion.

## Project Structure

### Documentation (this feature)
```text
specs/004-better-auth-integration/
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output (/sp.plan command)
├── data-model.md        # Phase 1 output (/sp.plan command)
├── quickstart.md        # Phase 1 output (/sp.plan command)
├── contracts/           # Phase 1 output (/sp.plan command)
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)
```text
backend/
├── app/
│   ├── main.py          # FastAPI app with Better Auth integration
│   ├── auth/            # Authentication-specific routes and logic
│   ├── models/          # Data models including user profiles
│   ├── services/        # Auth and user profile services
│   └── api/             # RAG API endpoints (unchanged)
└── tests/
    ├── auth/            # Authentication-specific tests
    └── api/             # RAG API tests (ensuring no auth blocking)

frontend/
├── src/
│   ├── pages/
│   │   ├── signup.js    # Signup page with background collection
│   │   └── signin.js    # Signin page
│   ├── components/
│   │   └── auth/        # Auth-related components
│   └── services/
│       └── auth.js      # Auth service using Better Auth client
└── docusaurus.config.js # Updated to include auth routes
```

**Structure Decision**: Selected Option 2 (Web application) as the feature involves both frontend (Docusaurus React) and backend (FastAPI) components. The authentication layer will be integrated into existing backend structure while maintaining isolation from RAG functionality.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| [None] | [No violations identified] | [All constitution checks passed] |