---
description: "Task list for Backend Foundations & OpenAI Agents SDK implementation"
---

# Tasks: Backend Foundations & OpenAI Agents SDK

**Input**: Design documents from `/specs/003-backend-foundations/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: The examples below include test tasks. Tests are OPTIONAL - only include them if explicitly requested in the feature specification.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Backend project**: `backend/` at repository root
- **Backend structure**: `backend/app/`, `backend/tools/`, `backend/ingestion/`, `backend/tests/`

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [X] T001 Create project structure: backend/, backend/app/, backend/tools/, backend/ingestion/, backend/tests/
- [X] T002 [P] Fetch latest documentation via Context7 MCP Server for: uv package manager, FastAPI, OpenAI Agents SDK, Gemini
- [X] T003 Initialize Python project with uv package manager and create isolated environment
- [X] T004 [P] Install core dependencies: FastAPI, OpenAI Agents SDK, Cohere, qdrant-client, psycopg2-binary, python-dotenv

---
## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [X] T005 [P] Create environment variable management in backend/app/config.py
- [X] T006 [P] Configure CORS middleware restricted to deployed book domain in backend/app/main.py
- [X] T007 [P] Create database connection setup for Neon Serverless Postgres in backend/app/database.py
- [X] T008 [P] Create Qdrant client setup in backend/app/vector_db.py
- [X] T009 [P] Create Cohere client setup in backend/app/embeddings.py
- [X] T010 Create base models: QueryRequest, QueryResponse, SourceReference in backend/app/models/
- [X] T011 [P] Create initial FastAPI app structure in backend/app/main.py
- [X] T012 [P] Configure logging and error handling infrastructure in backend/app/utils/

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - RAG Query Processing (Priority: P1) 🎯 MVP

**Goal**: A user submits a question to the RAG chatbot and receives a grounded response with citations from the book content or selected text using OpenAI Agents SDK with Gemini as the reasoning engine.

**Independent Test**: Can be fully tested by submitting a query and verifying that the response is grounded in provided context with proper citations.

### Tests for User Story 1 (Testing Phase)

- [ ] T022 [P] [US1] Create unit tests for agent service in backend/tests/unit/test_agent_service.py
- [ ] T023 [P] [US1] Create integration tests for query endpoint in backend/tests/integration/test_query_endpoint.py
- [ ] T024 [P] [US1] Create contract tests for /query API in backend/tests/contract/test_query_contract.py
- [ ] T035 [P] [US1] Create API validation tests for /query endpoint in backend/tests/validation/test_query_api.py

### Implementation for User Story 1

- [X] T025 [P] [US1] Create Agent service in backend/app/services/agent_service.py
- [X] T026 [P] [US1] Create Gemini LLM integration in backend/app/services/llm_service.py
- [X] T027 [P] [US1] Create Qdrant retrieval service in backend/app/services/retrieval_service.py
- [X] T028 [US1] Create grounding rules enforcement in backend/app/services/grounding_service.py
- [X] T029 [US1] Create citation generation in backend/app/services/citation_service.py
- [X] T030 [US1] Implement POST /query endpoint in backend/app/api/v1/query.py
- [X] T031 [US1] Implement context determination logic (Qdrant retrieval vs user-selected text)
- [X] T032 [US1] Implement "I don't know" response when context is insufficient
- [X] T033 [US1] Connect agent to /query endpoint and return structured JSON response

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently

---

## Phase 4: User Story 3 - API Endpoint Access (Priority: P3)

**Goal**: A frontend application connects to the backend API to submit queries, select text, retrieve source information, and trigger content ingestion with secure, restricted access to authorized domains.

**Independent Test**: Can be fully tested by making API calls to each endpoint and verifying proper responses.

### Tests for User Story 3 (Testing Phase)

- [ ] T034 [P] [US3] Create unit tests for select endpoint in backend/tests/unit/test_select_endpoint.py
- [ ] T035 [P] [US3] Create unit tests for sources endpoint in backend/tests/unit/test_sources_endpoint.py
- [ ] T036 [P] [US3] Create integration tests for all API endpoints in backend/tests/integration/test_api_endpoints.py
- [ ] T042 [P] [US3] Create API validation tests for /select and /sources endpoints in backend/tests/validation/test_api_validation.py

### Implementation for User Story 3

- [X] T037 [P] [US3] Implement POST /select endpoint in backend/app/api/v1/select.py
- [X] T038 [P] [US3] Implement GET /sources/{chunk_id} endpoint in backend/app/api/v1/sources.py
- [X] T039 [US3] Create chunk management service in backend/app/services/chunk_service.py
- [X] T040 [US3] Add source reference lookup functionality
- [X] T041 [US3] Add proper error handling for missing chunk IDs

**Checkpoint**: At this point, User Stories 1 AND 3 should both work independently

---

## Phase 5: User Story 2 - Content Ingestion & Processing (Priority: P2)

**Goal**: A system administrator ingests book content into the system, which processes the content, creates embeddings, and stores them in Qdrant for retrieval while ensuring content integrity and proper chunking.

**Independent Test**: Can be fully tested by ingesting content and verifying it's properly stored and retrievable from Qdrant.

### Tests for User Story 2 (Testing Phase)

- [ ] T042 [P] [US2] Create unit tests for sitemap parser in backend/tests/unit/test_sitemap_parser.py
- [ ] T043 [P] [US2] Create unit tests for content extractor in backend/tests/unit/test_content_extractor.py
- [ ] T044 [P] [US2] Create integration tests for ingestion pipeline in backend/tests/integration/test_ingestion_pipeline.py
- [ ] T045 [P] [US2] Create contract tests for /ingest API in backend/tests/contract/test_ingest_contract.py
- [ ] T050 [P] [US2] Create API validation tests for /ingest endpoint in backend/tests/validation/test_ingest_api.py

### Implementation for User Story 2

- [X] T046 [P] [US2] Create sitemap parser in backend/ingestion/sitemap_parser.py
- [X] T047 [P] [US2] Create content extractor in backend/ingestion/content_extractor.py
- [X] T048 [P] [US2] Create content chunker (400-700 tokens with overlap) in backend/ingestion/chunker.py
- [X] T049 [US2] Create embedding generation service using Cohere in backend/ingestion/embedding_service.py
- [X] T050 [US2] Create Qdrant storage service for embeddings in backend/ingestion/vector_storage.py
- [X] T051 [US2] Implement POST /ingest endpoint in backend/app/api/v1/ingest.py
- [X] T052 [US2] Implement ingestion job tracking and status in backend/app/services/ingestion_service.py
- [X] T053 [US2] Add content validation and integrity checks
- [X] T054 [US2] Implement retrieval verification for ingested content

**Checkpoint**: All user stories should now be independently functional

---

## Phase 6: Persistence & State Management

**Goal**: Ensure all session, metadata, and personalization data is stored in Neon Serverless Postgres with proper stateless agent behavior.

### Tests for Persistence (Testing Phase)

- [ ] T055 [P] Create unit tests for session management in backend/tests/unit/test_session_service.py
- [ ] T056 [P] Create unit tests for metadata persistence in backend/tests/unit/test_metadata_service.py
- [ ] T057 [P] Create integration tests for data persistence in backend/tests/integration/test_persistence.py

### Implementation for Persistence

- [X] T058 [P] Create Session model in backend/app/models/session.py
- [X] T059 [P] Create Chunk model in backend/app/models/chunk.py
- [X] T060 [P] Create User model in backend/app/models/user.py
- [X] T061 Create session management service in backend/app/services/session_service.py
- [X] T062 Create metadata persistence for agent interactions in backend/app/services/metadata_service.py
- [X] T063 Implement stateless agent behavior with Neon Postgres persistence
- [X] T064 Add user consent management for data storage

**Checkpoint**: All data persistence requirements are implemented

---

## Phase 7: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

### Testing Tasks (Added)

- [ ] T065 [P] Create end-to-end tests for User Story 1 in backend/tests/e2e/test_query_flow.py
- [ ] T066 [P] Create end-to-end tests for User Story 3 in backend/tests/e2e/test_api_endpoints.py
- [ ] T067 [P] Create end-to-end tests for User Story 2 in backend/tests/e2e/test_ingestion_flow.py
- [ ] T068 [P] Create system integration tests in backend/tests/system/test_full_system.py
- [ ] T069 [P] Create API validation tests in backend/tests/validation/test_api_validation.py

### Implementation Tasks

- [X] T070 [P] Add comprehensive error handling across all endpoints
- [X] T071 [P] Add request/response logging for all API endpoints
- [X] T072 Add performance monitoring and metrics
- [X] T073 [P] Documentation updates in backend/README.md
- [X] T074 Add input validation for all API endpoints
- [X] T075 Security hardening and API key validation
- [X] T076 Run quickstart.md validation to ensure setup instructions work
- [X] T077 [P] Add comprehensive tests for all implemented functionality

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3+)**: All depend on Foundational phase completion
  - User stories can then proceed in parallel (if staffed)
  - Or sequentially in priority order (P1 → P2 → P3)
- **Persistence (Phase 6)**: Depends on all user stories being complete
- **Polish (Final Phase)**: Depends on all desired user stories and persistence being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 3 (P3)**: Can start after Foundational (Phase 2) - May integrate with US1 but should be independently testable
- **User Story 2 (P2)**: Can start after Foundational (Phase 2) - May integrate with US1/US3 but should be independently testable
- **Persistence (Phase 6)**: Depends on all user stories to understand data requirements

### Within Each User Story

- Models before services
- Services before endpoints
- Core implementation before integration
- Story complete before moving to next priority

### Parallel Opportunities

- All Setup tasks marked [P] can run in parallel
- All Foundational tasks marked [P] can run in parallel (within Phase 2)
- Once Foundational phase completes, all user stories can start in parallel (if team capacity allows)
- Models within a story marked [P] can run in parallel
- Different user stories can be worked on in parallel by different team members

---

## Parallel Example: User Story 1

```bash
# Launch all components for User Story 1 together:
Task: "Create Agent service in backend/app/services/agent_service.py"
Task: "Create Gemini LLM integration in backend/app/services/llm_service.py"
Task: "Create Qdrant retrieval service in backend/app/services/retrieval_service.py"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3. Complete Phase 3: User Story 1
4. **STOP and VALIDATE**: Test User Story 1 independently
5. Deploy/demo if ready

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 → Test independently → Deploy/Demo (MVP!)
3. Add User Story 3 → Test independently → Deploy/Demo
4. Add User Story 2 → Test independently → Deploy/Demo
5. Add Persistence → Test independently → Deploy/Demo
6. Each story adds value without breaking previous stories

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together
2. Once Foundational is done:
   - Developer A: User Story 1
   - Developer B: User Story 3
   - Developer C: User Story 2
   - Developer D: Persistence layer
3. Stories complete and integrate independently

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Verify tests fail before implementing
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence