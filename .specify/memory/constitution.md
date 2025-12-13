<!--
Sync Impact Report:
- Version change: 2.1.0 → 3.0.0
- Summary: Complete overhaul of project principles to support the RAG Chatbot Integration. All previous principles are superseded.
- Added Principles:
  - Principle 1: Grounded & Reproducible AI
  - Principle 2: Mandated Technology Stack
  - Principle 3: Structured Development & Execution
  - Principle 4: Documentation & Verification
  - Principle 5: Backend & Frontend Standards
- Removed Principles:
  - All principles from v2.1.0 were removed and replaced.
- Templates requiring updates:
  - ✅ .specify/templates/plan-template.md (Checked, no update needed)
  - ✅ .specify/templates/spec-template.md (Checked, no update needed)
  - ✅ .specify/templates/tasks-template.md (Checked, no update needed)
- Follow-up TODOs: None
-->

# Constitution for RAG Chatbot Integration for a Published Docusaurus Course Book

## Preamble

This document outlines the governing principles, mandatory technologies, and development standards for the **RAG Chatbot Integration for a Published Docusaurus Course Book** project. Adherence to this constitution is mandatory for all project activities to ensure alignment, quality, and maintainability.

---

## 1. Governance

- **Constitution Version**: 3.0.0
- **Ratification Date**: 2025-12-12
- **Last Amended Date**: 2025-12-13
- **Amendment Process**: Changes require review and approval via a pull request. Major changes increment the version number.

---

## 2. Core Principles

### Principle 1: Grounded & Reproducible AI

- **Rule**: All AI-generated answers MUST be grounded in the Docusaurus course book content or user-selected text ONLY. The system is forbidden from using external knowledge, accessing the web for answers, or hallucinating information.
- **Rationale**: The primary function of the chatbot is to provide a faithful and accurate interface to the existing course material. Trust and reliability are paramount.

- **Rule**: All data pipelines for ingestion, retrieval, and inference MUST be reproducible.
- **Rationale**: Ensures that the AI's behavior is consistent and allows for debugging and auditing of the content processing and retrieval mechanisms.

### Principle 2: Mandated Technology Stack

- **Rule**: The project MUST use the following technologies. No substitutes are permitted.
  - **Embeddings**: Cohere
  - **Vector Database**: Qdrant Cloud (Free Tier)
  - **LLM**: Gemini
  - **Backend API**: FastAPI
  - **Backend Agent Framework**: OpenAI Agents SDK
  - **Frontend Chat UI**: OpenAI ChatKit SDK
  - **Metadata & Sessions**: Neon Serverless Postgres
  - **Containerization**: Docker
  - **Python Package Manager**: uv
  - **Documentation Source**: Context7 MCP Server
  - **Authentication**: Better Auth (to be implemented *after* core chatbot functionality is complete)
- **Rationale**: Standardization on a pre-vetted, modern stack ensures component compatibility, focuses development effort, and simplifies operational management. `uv` is chosen for its performance, and `Context7 MCP Server` is mandated to prevent API misuse.

### Principle 3: Structured Development & Execution

- **Rule**: Development MUST follow a strict, sequential, and chunked execution order.
  - **Phase 1 (Specs 1-4)**: Implement the end-to-end RAG chatbot functionality.
  - **Phase 2 (Post-Spec-4)**: Implement authentication and user persistence using Better Auth in separate, well-defined specs (5A, 5B, 5C).
- **Rationale**: This phased approach de-risks the project by focusing on delivering the core value proposition first. It prevents scope creep and ensures the foundational chatbot is stable before adding secondary features like authentication.

### Principle 4: Documentation & Verification

- **Rule**: Before using any SDK or external API, developers MUST fetch the latest, up-to-date documentation from the **Context7 MCP Server**. Guessing, using cached knowledge, or relying on web search for API contracts is forbidden.
- **Rationale**: APIs and SDKs evolve. The Context7 MCP Server acts as the single source of truth for dependencies, preventing bugs caused by outdated or incorrect API usage.

- **Rule**: A comprehensive environment documentation file MUST be maintained at `/docs/rag/env_urls.md`. It must list all service URLs, endpoints, and setup instructions, with all values verified against the Context7 MCP Server.
- **Rationale**: Centralizes critical configuration information, simplifying setup for new developers and ensuring consistency across environments.

### Principle 5: Backend & Frontend Standards

- **Rule (Backend)**: The backend MUST be a FastAPI application running in a Docker container with dependencies managed by `uv`. It must expose the specified endpoints (`/query`, `/select`, etc.), restrict CORS to the deployed book domain, and have no external web access.
- **Rationale**: Enforces a secure, isolated, and scalable backend architecture.

- **Rule (Frontend)**: The ChatKit UI MUST be themed to match the futuristic design of the Docusaurus book. It must support both general queries and Q&A based on user-selected text and render clear citations.
- **Rationale**: Provides a seamless and consistent user experience that feels like an integrated part of the course book.

### Principle 6: Privacy & Data Integrity

- **Rule**: The system MUST NOT store Personally Identifiable Information (PII) without explicit, affirmative user consent. The core RAG chatbot functionality must remain usable anonymously.
- **Rationale**: Protects user privacy and reduces compliance overhead.

- **Rule**: The RAG pipeline must use versioned collections in Qdrant, a chunk size between 400-700 tokens with overlap, and extract content source URLs from the book's sitemap.
- **Rationale**: Ensures data integrity, traceability, and optimal retrieval performance.
