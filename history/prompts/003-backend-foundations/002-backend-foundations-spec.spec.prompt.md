---
id: 002
title: Backend Foundations Spec Creation
stage: spec
date: 2025-12-18
surface: agent
model: Claude Sonnet 4.5
feature: 003-backend-foundations
branch: 003-backend-foundations
user: Claude Code User
command: /sp.specify
labels: ["spec", "backend", "fastapi", "openai-agents", "rag"]
links:
  spec: specs/003-backend-foundations/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - specs/003-backend-foundations/spec.md
  - specs/003-backend-foundations/checklists/requirements.md
tests:
  - none
---

## Prompt

spec-003 Backend Foundations & OpenAI Agents SDK
Purpose

Establish the backend foundation for the RAG chatbot:

Initialize Python project with uv package manager

Set up FastAPI backend

Integrate OpenAI Agents SDK using Gemini as the chat-completion model

All subsequent specs depend on this foundational setup.

Mandatory Steps
1. Initialize Backend Project

Use uv as the Python package manager

Create isolated project environment

Install base dependencies:

FastAPI

OpenAI Agents SDK

Any required adapters for Neon Postgres, Qdrant, Cohere

2. Initialize FastAPI Backend

Scaffold FastAPI project:

/app for main application

/tools for agent tools

/ingestion for content ingestion logic

/tests for automated tests

Configure environment variable management

Set up base endpoints:

POST /query
POST /select
GET  /sources/{chunk_id}
POST /ingest


Enable CORS restricted to deployed book domain

3. OpenAI Agents SDK Integration

Integrate OpenAI Agents SDK as the core reasoning layer

Gemini MUST be used as the chat-completion model for all responses

Agent responsibilities:

Receive queries from FastAPI

Determine context source:

Qdrant retrieval

User-selected text

Enforce strict grounding rules

Generate responses via Gemini

Include citations for each answer

Return structured output to FastAPI

Grounding Rules

Only use:

Qdrant-retrieved chunks

OR user-selected text

No external knowledge, browsing, or hallucinations

If context is insufficient, respond exactly:

"I don't know based on the provided text."

State & Persistence

Agent is stateless by default

Any session, metadata, or personalization data:

MUST be stored in Neon Serverless Postgres

MUST respect user consent

No implicit memory or hidden learning

Documentation Requirement

Before implementing FastAPI, uv setup, or OpenAI Agents SDK:

Fetch latest documentation via Context7 MCP Server

Use only documented APIs

No guessing or undocumented functionality

Output Schema
{
  "answer": "string",
  "citations": [
    {
      "chunk_id": "string",

## Response snapshot

Created the specification for Backend Foundations & OpenAI Agents SDK feature (003-backend-foundations). The spec includes:

- User stories for RAG query processing, content ingestion, and API endpoint access
- Functional requirements for initializing Python project with uv, setting up FastAPI, integrating OpenAI Agents SDK with Gemini
- Requirements for grounding responses, citation inclusion, and data storage in Neon Postgres
- Success criteria for response time, citation accuracy, and system behavior
- Quality validation checklist confirming spec completeness

The specification adheres to the constitution's requirements for using specific technologies (FastAPI, OpenAI Agents SDK, Gemini, Neon Postgres, Qdrant) and following grounding rules for RAG responses.

## Outcome

- ✅ Impact: Created foundational backend specification for RAG chatbot
- 🧪 Tests: none
- 📁 Files: specs/003-backend-foundations/spec.md, specs/003-backend-foundations/checklists/requirements.md
- 🔁 Next prompts: Continue with planning phase using /sp.plan
- 🧠 Reflection: Specification provides clear foundation for backend implementation with proper grounding and citation requirements

## Evaluation notes (flywheel)

- Failure modes observed: none
- Graders run and results (PASS/FAIL): N/A
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Begin implementation planning with /sp.plan