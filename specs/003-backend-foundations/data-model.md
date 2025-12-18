# Data Model: Backend Foundations & OpenAI Agents SDK

## Key Entities

### QueryRequest
- **Fields**:
  - `query`: string - The user's question or query text
  - `context`?: string - Optional additional context provided by user
  - `session_id`?: string - Optional session identifier for tracking
- **Relationships**: None
- **Validation**: Query must be non-empty

### QueryResponse
- **Fields**:
  - `answer`: string - The generated response to the query
  - `citations`: Array<SourceReference> - List of sources used in the response
  - `session_id`?: string - Optional session identifier
- **Relationships**: References SourceReference entities
- **Validation**: Citations must include valid chunk_id when answer is provided

### Chunk
- **Fields**:
  - `chunk_id`: string - Unique identifier for the content chunk
  - `content`: string - The actual text content of the chunk
  - `source_url`: string - URL where the content originated
  - `module`: string - Module/chapter where content appears
  - `anchor`?: string - Specific anchor/section within the source
  - `embedding`: Array<number> - Vector embedding of the content
  - `created_at`: timestamp - When the chunk was created
- **Relationships**: None
- **Validation**: Content must be 400-700 tokens, chunk_id must be unique

### SourceReference
- **Fields**:
  - `chunk_id`: string - Reference to the content chunk
  - `module`: string - Module/chapter where the content appears
  - `chapter`: string - Chapter name or identifier
  - `anchor`?: string - Specific anchor/section within the source
  - `url`: string - Full URL to the source
- **Relationships**: References Chunk entity
- **Validation**: Must have valid chunk_id and source information

### Session
- **Fields**:
  - `session_id`: string - Unique identifier for the session
  - `created_at`: timestamp - When the session was created
  - `updated_at`: timestamp - Last activity timestamp
  - `user_id`?: string - Optional user identifier (if authenticated)
- **Relationships**: May reference multiple QueryRequest/QueryResponse pairs
- **Validation**: Session ID must be unique

### User (Post-authentication)
- **Fields**:
  - `user_id`: string - Unique identifier for the user
  - `email`: string - User's email address
  - `consent`: boolean - Whether user has consented to data storage
  - `created_at`: timestamp - When the user account was created
- **Relationships**: May reference multiple sessions
- **Validation**: Email must be valid, consent required for data storage

## State Transitions

### Chunk State
- `PENDING`: Chunk has been extracted but not yet processed
- `EMBEDDING`: Embedding generation in progress
- `INDEXED`: Chunk has been indexed in Qdrant vector database
- `AVAILABLE`: Chunk is available for retrieval
- `DEPRECATED`: Chunk is no longer current (for versioning)

## Validation Rules

### Content Validation
- Chunk size: 400-700 tokens with overlap as specified in requirements
- No modification of original book content during processing
- Source references must be accurate and verifiable

### Query Validation
- Queries must be non-empty strings
- Responses must include proper citations when content is available
- "I don't know" response required when no relevant context exists

### Storage Validation
- All metadata must be stored in Neon Serverless Postgres
- Vector embeddings must be stored in Qdrant
- No PII stored without explicit user consent