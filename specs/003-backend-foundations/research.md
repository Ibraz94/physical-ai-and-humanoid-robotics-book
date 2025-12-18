# Research Summary: Backend Foundations & OpenAI Agents SDK

## Decision: Python Environment Setup with uv
- **Rationale**: Using uv as the package manager provides faster dependency resolution and installation compared to pip. It's the modern standard for Python project management.
- **Alternatives considered**: pip + venv, conda, poetry
- **Chosen approach**: uv for its speed and simplicity

## Decision: FastAPI Backend Framework
- **Rationale**: FastAPI provides automatic API documentation, type hints, async support, and high performance. It integrates well with the Python ecosystem.
- **Alternatives considered**: Flask, Django, Starlette
- **Chosen approach**: FastAPI for its modern features and developer experience

## Decision: OpenAI Agents SDK Integration
- **Rationale**: The OpenAI Agents SDK provides a structured way to create AI agents with memory, tools, and reasoning capabilities. Though the name suggests OpenAI, it can work with other LLM providers.
- **Alternatives considered**: LangChain, LlamaIndex, custom agent implementation
- **Chosen approach**: OpenAI Agents SDK as required by the constitution

## Decision: Gemini as Primary LLM
- **Rationale**: Constitution mandates the use of Gemini for all LLM reasoning and responses. This ensures compliance with project requirements.
- **Alternatives considered**: GPT-4, Claude, open-source models
- **Chosen approach**: Gemini as required by constitution

## Decision: Vector Database - Qdrant Cloud
- **Rationale**: Qdrant Cloud provides managed vector database capabilities with good performance and scalability. Free tier supports the initial development.
- **Alternatives considered**: Pinecone, Weaviate, Chroma
- **Chosen approach**: Qdrant Cloud (Free Tier) as required by constitution

## Decision: Embeddings - Cohere
- **Rationale**: Constitution mandates Cohere for embeddings generation, ensuring consistency with project requirements.
- **Alternatives considered**: OpenAI embeddings, Hugging Face models
- **Chosen approach**: Cohere as required by constitution

## Decision: Metadata Storage - Neon Serverless Postgres
- **Rationale**: Neon Serverless Postgres provides serverless PostgreSQL with git-like branching features, perfect for development and scaling.
- **Alternatives considered**: Supabase, PlanetScale, traditional PostgreSQL
- **Chosen approach**: Neon Serverless Postgres as required by constitution

## API Endpoint Design
- **POST /query**: Main endpoint for submitting queries to the RAG system
- **POST /select**: Endpoint for handling user-selected text
- **GET /sources/{chunk_id}**: Endpoint for retrieving source information for citations
- **POST /ingest**: Endpoint for triggering content ingestion process

## Grounding and Response Rules
- **Strict grounding**: Only use Qdrant-retrieved chunks OR user-selected text
- **Insufficient context response**: "I don't know based on the provided text."
- **Citation requirement**: Include chunk_id and source information with each response
- **Stateless design**: Agent is stateless by default, with session data in Neon Postgres