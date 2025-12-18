---
id: 001
title: RAG Chatbot Constitution Update
stage: constitution
date: 2025-12-18
surface: agent
model: Claude Sonnet 4.5
feature: none
branch: master
user: Claude Code User
command: /sp.constitution
labels: ["constitution", "rag", "chatbot", "database"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - .specify/memory/constitution.md
tests:
  - none
---

## Prompt

Here is the **revised Constitution Prompt**, explicitly and clearly stating **Neon Serverless Postgres as the database** everywhere it applies. This version **replaces** the earlier one and should be treated as the authoritative constitution.

---

# 📜 RAG Chatbot Constitution Prompt

## Role & Authority

You are an **Autonomous Senior RAG Systems Architect & Implementer** responsible for designing, building, and integrating a **Retrieval-Augmented Generation (RAG) chatbot** into a **published Docusaurus course book**.

You must strictly follow this constitution.
**Deviation, assumption, hallucination, or undocumented API usage is prohibited.**

---

## Core Mission

Build a **production-grade, privacy-first RAG chatbot** that:

* Answers questions **only from the book content or user-selected text**
* Is fully reproducible end-to-end
* Is embedded into the existing Docusaurus frontend
* Uses **only the mandated technologies**
* Enforces strict grounding and citation
* Uses **Neon Serverless Postgres as the sole relational database**
* Is extensible with authentication **only after RAG completion**

---

## Mandatory Execution Order

### Phase 1 — RAG Core (Non-Negotiable)

You MUST complete these specs in order:

1. **Spec-1 → Spec-4**

   * Sitemap ingestion
   * Chunking & embeddings
   * Vector storage & retrieval
   * Grounded answering with citations
   * Frontend + backend integration

🚫 **Authentication is forbidden before Spec-4 succeeds**

---

### Phase 2 — Authentication (Post-RAG Only)

Only after Spec-4 passes:

* **Spec-5A** — Better Auth Setup
* **Spec-5B** — Session & User Persistence
* **Spec-5C** — Optional Protected Features

Anonymous chatbot access must **always remain functional**.

---

## Grounding & Truth Rules (Absolute)

* Answers MUST be grounded in:

  * Qdrant-retrieved chunks
  * OR user-selected text
* **No external knowledge**
* **No browsing**
* **No assumptions**
* **No hallucinations**

If context is insufficient, respond EXACTLY:

> **"I don't know based on the provided text."**

---

## Mandatory Technologies (No Substitutions)

| Layer                        | Technology                               |
| ---------------------------- | ---------------------------------------- |
| Embeddings                   | **Cohere**                               |
| Vector Database              | **Qdrant Cloud (Free Tier)**             |
| Relational Database          | **Neon Serverless Postgres (MANDATORY)** |
| LLM                          | **Gemini (all reasoning & answers)**     |
| Backend Framework            | **FastAPI**                              |
| Backend Agent                | **OpenAI Agents SDK (mandatory)**        |
| Frontend Chat UI             | **OpenAI ChatKit SDK**                   |
| Package Manager              | **uv**                                   |
| Containerization             | **Docker**                               |
| Authentication (Post-Spec-4) | **Better Auth**                          |
| Documentation Source         | **Context7 MCP Server**                  |

🚫 No alternatives allowed.

---

## Documentation Rule (Global & Mandatory)

Before using **ANY** SDK, API, or framework:

1. **Fetch the latest documentation via Context7 MCP Server**
2. Verify:

   * API signatures
   * Configuration patterns
   * Required environment variables
3. Implement **only documented behavior**

🚫 Guessing undocumented APIs is forbidden.

---

## RAG Pipeline Rules

### Content Source

* URLs extracted ONLY from:

```
<book-url>/sitemap
```

---

### Chunking

* Chunk size: **400–700 tokens**
* Overlap required
* Book content is **read-only** and must not be altered

---

### Embeddings

* Generated ONLY using **Cohere**
* Stored ONLY in **Qdrant**

---

### Vector Storage

* Versioned Qdrant collection registry is required
* No re-ingestion without version bumping

---

## Retrieval & Answering Rules

* Context passed to Gemini MUST be strictly limited to:

  * Retrieved Qdrant chunks
  * OR user-selected text
* Gemini must be **hard-constrained to context**
* All answers MUST include citations:

  * Module / Chapter / Anchor
* No citation → No answer

---

## Backend Standards

### Required FastAPI Endpoints

```
POST /query
POST /select
GET  /sources/{chunk_id}
POST /ingest
```

---

### Backend Constraints

* Backend MUST:

  * Use **FastAPI**
  * Use **OpenAI Agents SDK**
  * Use **Neon Serverless Postgres** for:

    * Metadata
    * Ingestion state
    * Chunk registry
    * User sessions (post-auth)
    * Optional chat history
* No external web access
* CORS restricted to deployed book domain
* All configuration via environment variables

---

## Frontend Standards

* Built into the existing **Docusaurus site**
* Chat UI implemented using **OpenAI ChatKit SDK**
* UI must match the book's futuristic design system
* Must support:

  * Selected-text Q&A
  * Source citations
* Backend API URL loaded via environment variables

---

## Authentication Rules (Post-Spec-4 Only)

### Better Auth Integration

* Implement signup & signin using:

```
https://www.better-auth.com/
```

* During signup, collect:

  * Software background
  * Hardware background

* User background data:

  * Stored ONLY in **Neon Serverless Postgres**
  * Used ONLY for content personalization
  * Requires explicit user consent
  * Must never block anonymous access

---

### Persistence Rules

* Authenticated users:

  * Linked to records in **Neon Serverless Postgres**
  * Sessions stored in Neon
  * Chat history stored only if user opts in
* Anonymous users:

  * Fully supported
  * No PII stored

---

## Required Directory Structure

```
frontend/
  └─ Docusaurus + ChatKit UI

backend/
  ├─ app/
  ├─ tools/
  ├─ ingestion/
  └─ tests/
```

---

## Environment Documentation (Mandatory)

Create and maintain:

```
/docs/rag/env_urls.md
```

Must include:

* Sitemap URL
* Qdrant endpoint
* Cohere endpoint
* Gemini endpoint
* **Neon Serverless Postgres connection URL**
* Backend API URL
* Frontend URL
* uv setup instructions
* Better Auth

## Response snapshot

Updated the project constitution at `.specify/memory/constitution.md` to reflect the RAG Chatbot Constitution with specific principles around grounded responses, mandatory technology stack compliance, documentation-first development, RAG pipeline integrity, execution order compliance, and privacy-first architecture. The constitution now serves as the authoritative guide for building the RAG chatbot with Neon Serverless Postgres as the sole relational database.

## Outcome

- ✅ Impact: Updated project constitution with RAG-specific principles and constraints
- 🧪 Tests: none
- 📁 Files: .specify/memory/constitution.md updated
- 🔁 Next prompts: Continue with RAG implementation following new constitution
- 🧠 Reflection: Constitution now provides clear guidance for RAG chatbot development with mandatory technology stack and execution order

## Evaluation notes (flywheel)

- Failure modes observed: none
- Graders run and results (PASS/FAIL): N/A
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Begin RAG implementation following Spec-1 to Spec-4 sequence