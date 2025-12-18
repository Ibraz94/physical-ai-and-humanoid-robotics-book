# Feature Specification: Backend Foundations & OpenAI Agents SDK

**Feature Branch**: `003-backend-foundations`
**Created**: 2025-12-18
**Status**: Draft
**Input**: User description: "spec-003 Backend Foundations & OpenAI Agents SDK
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
      "chunk_id": "string"
"

## User Scenarios & Testing *(mandatory)*

### User Story 1 - RAG Query Processing (Priority: P1)

A user submits a question to the RAG chatbot and receives a grounded response with citations from the book content or selected text. The system uses the OpenAI Agents SDK with Gemini as the reasoning engine to process the query and ensure responses are strictly based on provided context.

**Why this priority**: This is the core functionality of the RAG chatbot - without this, the system has no value.

**Independent Test**: Can be fully tested by submitting a query and verifying that the response is grounded in provided context with proper citations.

**Acceptance Scenarios**:

1. **Given** a user has submitted a query and relevant context is available, **When** the query is processed by the agent, **Then** a response is generated that is grounded in the provided context with proper citations
2. **Given** a user has submitted a query and no relevant context is available, **When** the query is processed by the agent, **Then** the response is "I don't know based on the provided text."

---

### User Story 2 - Content Ingestion & Processing (Priority: P2)

A system administrator ingests book content into the system, which processes the content, creates embeddings, and stores them in Qdrant for retrieval. The system ensures content integrity and proper chunking for optimal retrieval.

**Why this priority**: This enables the core RAG functionality by providing the content that will be used for grounding responses.

**Independent Test**: Can be fully tested by ingesting content and verifying it's properly stored and retrievable from Qdrant.

**Acceptance Scenarios**:

1. **Given** book content is available at sitemap URLs, **When** the ingestion process is triggered, **Then** content is properly chunked (400-700 tokens with overlap) and stored in Qdrant with embeddings
2. **Given** content has been ingested, **When** a retrieval request is made, **Then** relevant chunks are returned based on the query

---

### User Story 3 - API Endpoint Access (Priority: P3)

A frontend application connects to the backend API to submit queries, select text, retrieve source information, and trigger content ingestion. The API provides secure, restricted access to authorized domains.

**Why this priority**: This enables the frontend to interact with the backend functionality.

**Independent Test**: Can be fully tested by making API calls to each endpoint and verifying proper responses.

**Acceptance Scenarios**:

1. **Given** a valid query is sent to POST /query, **When** the request is processed, **Then** a grounded response with citations is returned
2. **Given** a valid text selection is sent to POST /select, **When** the request is processed, **Then** the system processes the selected text appropriately
3. **Given** a chunk ID is requested via GET /sources/{chunk_id}, **When** the request is processed, **Then** source information is returned
4. **Given** an ingestion request is sent to POST /ingest, **When** the request is processed, **Then** content ingestion is initiated

---

## Edge Cases

- What happens when Qdrant vector database is unavailable during query processing?
- How does the system handle malformed queries or invalid context?
- What occurs when the Gemini API is temporarily unavailable?
- How does the system respond to queries when no relevant content is found in Qdrant?

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST initialize a Python project using uv as the package manager with isolated environment
- **FR-002**: System MUST set up a FastAPI backend with proper configuration and environment variable management
- **FR-003**: System MUST integrate OpenAI Agents SDK as the core reasoning layer with Gemini as the chat-completion model
- **FR-004**: System MUST provide four required endpoints: POST /query, POST /select, GET /sources/{chunk_id}, POST /ingest
- **FR-005**: System MUST enable CORS restricted to the deployed book domain only
- **FR-006**: System MUST enforce strict grounding rules using only Qdrant-retrieved chunks OR user-selected text
- **FR-007**: System MUST respond with "I don't know based on the provided text." when context is insufficient
- **FR-008**: System MUST include proper citations (chunk_id, module/chapter/anchor) with each response
- **FR-009**: System MUST store session, metadata, and personalization data in Neon Serverless Postgres
- **FR-010**: System MUST respect user consent for data storage and processing
- **FR-011**: System MUST be stateless by default with no implicit memory or hidden learning

### Key Entities

- **QueryRequest**: Represents a user query with context information, including the question text and any provided context
- **QueryResponse**: Contains the answer string and array of citations with chunk_id and source information
- **Chunk**: Represents a piece of content from the book with unique ID, text content, and source metadata
- **SourceReference**: Contains information about where content originated (module/chapter/anchor) for citation purposes

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: System can successfully process queries with grounded responses in under 5 seconds response time
- **SC-002**: 100% of responses include proper citations when content is available in the knowledge base
- **SC-003**: System correctly responds with "I don't know based on the provided text." when no relevant context is available
- **SC-004**: All API endpoints are accessible and return appropriate responses for valid requests
- **SC-005**: Content ingestion process successfully processes and stores book content with proper embeddings
- **SC-006**: CORS restrictions prevent access from unauthorized domains while allowing the book domain
- **SC-007**: System maintains stateless operation with all required data properly stored in Neon Postgres