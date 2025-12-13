---
id: 0002
title: Update Constitution for RAG Chatbot
stage: constitution
date: 2025-12-13
surface: agent
model: gemini
feature: none
branch: master
user: {{USER}}
command: /sp.constitution
labels: [constitution, rag, chatbot]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
 - .specify/memory/constitution.md
tests:
 (none)
---

## Prompt

$ARGUMENTS
```text
/sp.constitution Project:RAG Chatbot Integration for a Published Docusaurus Course BookExecution Order (Mandatory):1. Spec-1 → Spec-4: Complete RAG chatbot end-to-end.2. ONLY after Spec-4 succeeds, implement authentication using Better Auth   in separate, chunked specs.Core Principles:- All answers must be grounded in book content or user-selected text only.- No external knowledge, browsing, or hallucination.- Reproducible pipelines for ingestion, retrieval, and inference.- Clear citations (module/chapter anchors).- Privacy-first: no PII storage without explicit consent.- UI consistency with the book’s futuristic design.- **Always use Context7 MCP Server to fetch up-to-date documentation  for SDKs, APIs, and frameworks before implementation.**Mandatory Technologies:- Cohere → embeddings- Qdrant Cloud Free Tier → vector database- Gemini → LLM for all agent reasoning and responses- FastAPI → backend API server- OpenAI Agents SDK → backend agent (mandatory)- OpenAI ChatKit SDK → frontend chatbot UI- Neon Serverless Postgres → metadata, sessions, selections- Docker → backend containerization- **uv → Python package manager**- **Context7 MCP Server → documentation source of truth**- **Better Auth → authentication (post-chatbot only)**- Environment variables → all configurationRequired Directory Structure:- frontend/ → existing Docusaurus site + ChatKit UI- backend/ → RAG backend    • app/    • tools/    • ingestion/    • tests/RAG Pipeline Rules:- URLs extracted from `<book-url>/sitemap`- Chunk size: 400–700 tokens with overlap- Embeddings generated only with Cohere- Vectors stored only in Qdrant- Versioned collection registry requiredRetrieval & Answering Rules:- Context limited to:    • Qdrant-retrieved chunks    • OR user-selected text- Gemini must answer using only provided context.- If insufficient information, respond:  “I don’t know based on the provided text.”Backend Standards:- FastAPI endpoints:    • POST /query    • POST /select    • GET /sources/{chunk_id}    • POST /ingest- Backend agent MUST use OpenAI Agents SDK.- No external web access.- CORS restricted to deployed book domain.Frontend Standards:- ChatKit UI must match book theme.- Support selected-text Q&A and citations.- Backend URL loaded via environment variables.Documentation Rule (Global):- **Before implementing any SDK or API usage,  developers MUST fetch the latest documentation via Context7 MCP Server.**- No guessing or hallucinating undocumented APIs.Post-Spec-4: Better Auth (Chunked Specs)----------------------------------------Spec-5A — Better Auth Setup- Integrate Better Auth for sign-up and sign-in.- Configure providers and environment variables.- Auth system must not break existing chatbot access.Spec-5B — Session & User Persistence- Link authenticated users to Neon Postgres.- Store user sessions and optional chat history.- Ensure anonymous chatbot usage remains possible.Spec-5C — Protected Features (Optional)- Gate optional features (saved chats, history, preferences).- Core RAG chatbot must remain usable without auth.Environment Documentation:- `/docs/rag/env_urls.md` required.- Must include:    • sitemap URL    • Qdrant, Cohere, Gemini endpoints    • Neon DB URL    • backend API URL    • frontend URL    • uv setup    • Better Auth config (post-Spec-4)- All references verified via Context7 MCP Server.Constraints:- Book content must not change.- No alternative LLMs, embeddings, vector DBs, or auth providers.- No PII storage without consent.- No hallucinated or ungrounded answers.Success Criteria:- RAG chatbot fully integrated and working after Spec-4.- Accurate retrieval and citations.- Selection-only mode enforced.- Backend runs in Docker with uv-managed dependencies.- Frontend and backend integrated successfully.- Better Auth implemented cleanly in post-Spec-4 chunks.- Complete, MCP-verified environment documentation exists.
```

## Response snapshot

Updated the project constitution to version 3.0.0, replacing all previous principles with a new set tailored for the RAG Chatbot Integration project. The new constitution defines the mandated technology stack, development process, AI grounding rules, and documentation standards.

## Outcome

- ✅ Impact: Major overhaul of project governance to align with new project goals.
- 🧪 Tests: N/A
- 📁 Files: 1 file modified
- 🔁 Next prompts: (none)
- 🧠 Reflection: The user provided a very detailed set of requirements, which made creating the new constitution straightforward. The changes were significant, justifying a major version bump.

## Evaluation notes (flywheel)

- Failure modes observed: (none observed)
- Graders run and results (PASS/FAIL): PASS
- Prompt variant (if applicable): (none)
- Next experiment: (none)