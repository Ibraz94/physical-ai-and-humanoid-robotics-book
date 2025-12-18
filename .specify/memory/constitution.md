<!--
SYNC IMPACT REPORT:
Version change: N/A -> 1.0.0
Added sections: All principles and sections specific to RAG Chatbot
Removed sections: Template placeholders
Templates requiring updates: ⚠ pending (.specify/templates/plan-template.md, .specify/templates/spec-template.md, .specify/templates/tasks-template.md)
Follow-up TODOs: RATIFICATION_DATE to be set when officially adopted
-->
# RAG Chatbot for Docusaurus Course Book Constitution

## Core Principles

### Grounded Response Constraint
Answers must be grounded in Qdrant-retrieved chunks OR user-selected text; No external knowledge, browsing, assumptions, or hallucinations; Reply "I don't know based on the provided text" if context is insufficient. This ensures strict adherence to the book content and prevents any hallucinations or external knowledge usage.

### Mandatory Technology Stack Compliance
Must use Cohere for embeddings, Qdrant Cloud (Free Tier) for vector DB, Neon Serverless Postgres for metadata/sessions/personalization, Gemini for all LLM reasoning & answers, FastAPI for backend, OpenAI Agents SDK for backend agent, OpenAI ChatKit SDK for frontend UI, uv for Python package management, Docker for containerization, Better Auth for authentication (post-Spec-4), and Context7 MCP Server for documentation source of truth. No substitutions are allowed under any circumstances.

### Documentation-First Development
Before using any SDK, API, or framework, fetch and verify documentation via Context7 MCP Server. Verify API signatures, configuration patterns, and required environment variables. No guessed or undocumented usage is permitted. This ensures implementation follows only documented behavior and prevents assumptions about APIs.

### RAG Pipeline Integrity
Content URLs must be extracted only from <book-url>/sitemap, chunk size must be 400-700 tokens with overlap required, embeddings must be generated only with Cohere, vectors must be stored only in Qdrant, and versioned Qdrant collections are required. Book content is read-only and must not be altered during processing.

### Execution Order Compliance
Complete Spec-1 to Spec-4 (RAG core: ingestion, retrieval, answering, UI integration) before implementing authentication. Only after Spec-4 passes should authentication be implemented in phases: Spec-5A (Better Auth setup), Spec-5B (User & session persistence), and Spec-5C (Optional protected features). Anonymous chatbot access must always remain functional regardless of authentication features.

### Privacy-First Architecture
Neon Serverless Postgres must be used as the sole relational database for all metadata, ingestion state, chunk registry, user sessions (post-auth), and optional chat history. No PII should be stored without explicit user consent. Anonymous usage must remain available at all times, ensuring privacy-first design principles are maintained.

## Backend and Frontend Standards
Backend must implement required FastAPI endpoints: POST /query, POST /select, GET /sources/{chunk_id}, POST /ingest. The backend agent must use OpenAI Agents SDK, all metadata must be stored in Neon Serverless Postgres, no external web access is allowed, and CORS must be restricted to the deployed book domain. Frontend must be integrated into the existing Docusaurus site using OpenAI ChatKit SDK, match the book's futuristic design, and support selected-text Q&A with source citations.

## Development Workflow
All RAG pipeline components must be reproducible end-to-end. Answers from Gemini must be strictly limited to retrieved Qdrant chunks or user-selected text, with hard constraints preventing context violations. All answers must include citations (Module/Chapter/Anchor), and no citation means no answer is provided. Authentication features (Better Auth) must collect software and hardware background during signup and store user data only in Neon Serverless Postgres with explicit consent.

## Governance
This constitution supersedes all other practices, guidelines, and convenience considerations. All implementations must verify compliance with these principles before proceeding. All work must strictly follow documented APIs verified through Context7 MCP Server. All pull requests and reviews must verify constitutional compliance. If any rule conflicts with convenience, this Constitution overrides everything.

**Version**: 1.0.0 | **Ratified**: TODO(ratification_date): Original adoption date unknown | **Last Amended**: 2025-12-18
