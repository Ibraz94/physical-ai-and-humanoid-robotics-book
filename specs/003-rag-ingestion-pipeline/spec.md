# Feature Specification: RAG Ingestion Pipeline

**Feature Branch**: `003-rag-ingestion-pipeline`  
**Created**: 2025-12-13
**Status**: Draft  
**Input**: User description: "Spec-3 — Sitemap Extraction, Embeddings, Qdrant IndexingObjective:Prepare all book content for RAG by extracting deployed URLs from the book’s`/sitemap`, converting content into chunks, generating embeddings, and storingthem in Qdrant. This spec establishes the entire retrieval foundation.Scope:- Read-only interaction with the existing book in `frontend/`- All ingestion and indexing logic implemented inside `backend/ingestion/`Success Criteria:- All content URLs extracted from `<book-url>/sitemap`- Book content successfully extracted and cleaned- Content chunked into 400–700 token segments with overlap- Embeddings generated using Cohere only- Qdrant Cloud collection created and populated- Metadata stored for each chunk: • chunk_id • module / chapter / slug • preview text • embedding model version - Versioned `collection_registry.json` created- `docs/rag/env_urls.md` created with setup stepsConstraints:- Book content must NOT be modified- Cohere is the only embedding provider- Qdrant Cloud Free Tier is the only vector database- No retrieval logic, agents, LLM calls, or UI work- No authentication (Better Auth comes later)- No FastAPI endpoints in this specDocumentation Rule:- Use Context7 MCP Server to confirm: • Cohere embedding model usage • Qdrant ingestion APIs- Do not guess undocumented APIsNot Included:- Retrieval pipeline- OpenAI Agents SDK- Gemini usage- ChatKit UI- Docker runtime- AuthenticationDeliverables:- backend/ingestion/extract_urls.py (reads `/sitemap`)- backend/ingestion/extract_content.py- backend/ingestion/chunk_content.py- backend/ingestion/generate_embeddings.py- backend/ingestion/ingest_qdrant.py- backend/collection_registry.json- docs/rag/env_urls.md"

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Content Extraction and Preparation (Priority: P1)

As a system administrator, I need to extract all content URLs from the book's sitemap, process the corresponding content, and break it into standardized chunks so that it is ready for the embedding process.

**Why this priority**: This is the foundational first step. Without clean, chunked content, no further processing in the RAG pipeline is possible.

**Independent Test**: This can be tested by running the extraction and chunking scripts (`extract_urls.py`, `extract_content.py`, `chunk_content.py`) and verifying that they produce a set of structured, chunked text files from the sitemap URL.

**Acceptance Scenarios**:

1. **Given** a valid book sitemap URL, **When** the URL extraction script is run, **Then** a list of all content page URLs is generated.
2. **Given** a list of content URLs, **When** the content extraction and cleaning script is run, **Then** the raw text content from each page is saved locally.
3. **Given** the raw text content, **When** the chunking script is run, **Then** the content is divided into text segments between 400 and 700 tokens with overlap.

---

### User Story 2 - Embedding Generation and Vector Storage (Priority: P2)

As a system administrator, I need to take the prepared content chunks, generate vector embeddings for them using Cohere, and store them in the Qdrant Cloud vector database along with their metadata.

**Why this priority**: This step makes the content discoverable for the retrieval part of the RAG pipeline.

**Independent Test**: This can be tested by providing the chunked content to the embedding and ingestion scripts (`generate_embeddings.py`, `ingest_qdrant.py`) and verifying that the vectors and associated metadata appear correctly in the specified Qdrant Cloud collection.

**Acceptance Scenarios**:

1. **Given** a set of content chunks, **When** the embedding script is run, **Then** Cohere embeddings are generated for each chunk.
2. **Given** chunks with their embeddings, **When** the ingestion script is run, **Then** a new collection is created in Qdrant Cloud and populated with the vectors and their corresponding metadata.
3. **Given** an ingested chunk, **When** inspecting its entry in Qdrant, **Then** its metadata (chunk_id, module, slug, preview, model version) is present and accurate.

---

### User Story 3 - Registry and Documentation (Priority: P3)

As a developer, I need a versioned registry of all vector collections and clear documentation on the environment setup so that the ingestion process is repeatable and the project is easy to configure.

**Why this priority**: This ensures the data pipeline is maintainable, auditable, and easy for other developers to set up and use.

**Independent Test**: This can be tested by running the full ingestion pipeline and checking for the creation and correct content of `collection_registry.json` and `docs/rag/env_urls.md`.

**Acceptance Scenarios**:

1. **Given** a successful run of the ingestion pipeline, **When** the process completes, **Then** a `backend/collection_registry.json` file is created that lists the name and version of the newly created Qdrant collection.
2. **Given** the project setup, **When** a developer consults the documentation, **Then** a `docs/rag/env_urls.md` file exists and contains all necessary setup steps and environment variable descriptions for the ingestion pipeline.

---

### Edge Cases

- What happens if the book's sitemap URL is unreachable or invalid? The script should fail gracefully with a clear error message.
- How does the system handle a failure during the Cohere API call (e.g., network error, invalid API key)? The process should stop and log the error without leaving the Qdrant collection in a partially updated state.
- What happens if a content page from the sitemap is empty or cannot be parsed? The system should log a warning for that specific URL and continue processing the rest.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST extract all content URLs from the book's `/sitemap.xml`.
- **FR-002**: System MUST process and clean the HTML content from each URL to extract plain text.
- **FR-003**: System MUST split the extracted text into chunks of 400-700 tokens with a defined overlap.
- **FR-004**: System MUST generate vector embeddings for each text chunk using the Cohere API.
- **FR-005**: System MUST create a collection in Qdrant Cloud and store each chunk's embedding.
- **FR-006**: System MUST store a metadata payload with each vector, including `chunk_id`, `module/chapter/slug`, a `preview_text`, and the `embedding_model_version`.
- **FR-007**: System MUST create a versioned `collection_registry.json` file in the `backend/` directory to track created collections.
- **FR-008**: System MUST create a `docs/rag/env_urls.md` file detailing the setup and environment variables required for the pipeline.
- **FR-009**: The ingestion logic MUST be implemented within the `backend/ingestion/` directory.
- **FR-010**: The system MUST NOT modify the existing book content in the `frontend/` directory.

### Key Entities *(include if feature involves data)*

- **Content Chunk**: A segment of text (400-700 tokens) derived from a book content page. It is associated with a vector embedding and metadata that provides its source context (module, chapter, etc.).

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: 100% of the URLs present in the book's sitemap are processed by the ingestion pipeline.
- **SC-002**: A new collection is successfully created and populated in the specified Qdrant Cloud instance, containing a vector for every generated content chunk.
- **SC-003**: Each vector entry in Qdrant contains a complete metadata payload (chunk_id, source location, preview, model version).
- **SC-004**: A `collection_registry.json` file is generated with a valid entry for the new Qdrant collection.
- **SC-005**: A `docs/rag/env_urls.md` documentation file is created and contains all the necessary setup information.
