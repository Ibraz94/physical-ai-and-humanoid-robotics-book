"""
Agent service implementing OpenAI Agents SDK with Gemini integration via LiteLLM
"""
from typing import Dict, Any, Optional, List
from agents import Agent, Runner
from agents.extensions.models.litellm_model import LitellmModel
from ..models.query import QueryRequest, QueryResponse
from ..models.source import SourceReference
from ..utils.exceptions import ContextInsufficientException
from .llm_service import GeminiService
from .retrieval_service import RetrievalService
from .citation_service import CitationService
import logging
import os

logger = logging.getLogger(__name__)

class AgentService:
    def __init__(self):
        self.gemini_service = GeminiService()
        self.retrieval_service = RetrievalService()
        self.citation_service = CitationService()

        # Create the main agent using OpenAI Agents SDK with LiteLLM model that routes to Gemini
        self.agent = Agent(
            name="RAG Chatbot Agent",
            instructions="""You are a helpful AI assistant for a Physical AI and Humanoid Robotics course.

CRITICAL RULES:
1. Answer using ONLY the provided context
2. Keep answers SHORT and CONCISE (2-3 sentences maximum)
3. Use PLAIN TEXT only - NO markdown, NO bullet points, NO bold/italic, NO special formatting
4. Write in a natural, conversational tone
5. Do NOT include chunk_id, module, chapter, or anchor references
6. Do NOT add citations, sources, or references
7. If context is insufficient, say "I don't know based on the provided text."
8. Never use external knowledge

Write a brief, plain-text answer only.""",
            model=LitellmModel(model="gemini/gemini-2.5-flash", api_key=os.getenv("GEMINI_API_KEY")),
        )

    async def process_query(self, query_request: QueryRequest) -> QueryResponse:
        """
        Process a user query using OpenAI Agents SDK with Gemini
        """
        logger.info(f"[AgentService] Processing query: {query_request.query[:50]}...")

        try:
            # Determine context source (Qdrant retrieval or user-selected text)
            context_chunks = []

            if query_request.context and isinstance(query_request.context, dict):
                context_type = query_request.context.get('type', 'qdrant')
                
                if context_type == 'user_selected':
                    # User provided specific context (selected text)
                    user_text = query_request.context.get('content', '')
                    context_chunks = await self.retrieval_service.process_user_selected_text(user_text)
                else:
                    # Retrieve from Qdrant with filters
                    filters = query_request.context.get('filters')
                    max_chunks = query_request.context.get('max_chunks', 10)
                    context_chunks = await self.retrieval_service.retrieve_relevant_chunks(
                        query_request.query,
                        filters=filters,
                        limit=max_chunks
                    )
            else:
                # Default: Retrieve from Qdrant
                context_chunks = await self.retrieval_service.retrieve_relevant_chunks(query_request.query)

            logger.info(f"[AgentService] Retrieved {len(context_chunks)} context chunks")

            if not context_chunks:
                # No context available - return insufficient context response
                logger.info("[AgentService] No chunks retrieved - returning insufficient context")
                return QueryResponse(
                    answer="I don't know based on the provided text.",
                    citations=[],
                    session_id=query_request.session_id
                )

            # Prepare context for the agent
            context_str = "\n\n".join([
                f"[Source: {chunk.get('module', 'Unknown')} - {chunk.get('chapter', 'Unknown')}]\n{chunk['content']}"
                for chunk in context_chunks
            ])

            full_prompt = f"""Context from course materials:
{context_str}

User Question: {query_request.query}

Answer the question using ONLY the information from the context above."""

            # Use OpenAI Agents SDK Runner with Gemini via LiteLLM
            logger.info(f"[AgentService] Running agent with {len(context_chunks)} chunks...")
            result = await Runner.run(self.agent, full_prompt)

            # Extract answer from agent result
            answer = result.final_output
            logger.info(f"[AgentService] Agent response generated (length: {len(answer)})")

            # Generate citations
            citations = self.citation_service.generate_citations(context_chunks)

            # Create and return the response
            response = QueryResponse(
                answer=answer,
                citations=citations,
                session_id=query_request.session_id
            )

            return response

        except Exception as e:
            logger.error(f"[AgentService] Error processing query: {e}")
            import traceback
            traceback.print_exc()
            return QueryResponse(
                answer="I don't know based on the provided text.",
                citations=[],
                session_id=query_request.session_id
            )

