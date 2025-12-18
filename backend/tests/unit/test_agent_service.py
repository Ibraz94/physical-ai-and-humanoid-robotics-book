import pytest
from unittest.mock import Mock, patch, AsyncMock
from backend.app.services.agent_service import AgentService
from backend.app.models.query import QueryRequest, QueryResponse
from backend.app.services.grounding_service import GroundingService
from backend.app.services.citation_service import CitationService


class TestAgentService:
    """Unit tests for the AgentService class"""

    @pytest.fixture
    def agent_service(self):
        """Create an AgentService instance for testing"""
        return AgentService()

    @pytest.mark.asyncio
    async def test_process_query_with_sufficient_context(self, agent_service):
        """Test that the agent processes queries with sufficient context"""
        query_request = QueryRequest(query="What are the key principles of RAG systems?", context="Some context here")

        with patch.object(agent_service.llm_service, 'generate_response', return_value="RAG systems combine retrieval and generation"):
            with patch.object(agent_service.retrieval_service, 'retrieve_chunks', return_value=["chunk1", "chunk2"]):
                with patch.object(GroundingService, 'validate_response', return_value=True):
                    with patch.object(CitationService, 'generate_citations', return_value=["source1", "source2"]):
                        response = await agent_service.process_query(query_request)

                        assert isinstance(response, QueryResponse)
                        assert response.answer == "RAG systems combine retrieval and generation"
                        assert len(response.citations) > 0

    @pytest.mark.asyncio
    async def test_process_query_with_insufficient_context(self, agent_service):
        """Test that the agent returns 'I don't know' when context is insufficient"""
        query_request = QueryRequest(query="What is the meaning of life?", context="Irrelevant context")

        with patch.object(agent_service.llm_service, 'generate_response', return_value="I don't know based on the provided text."):
            with patch.object(agent_service.retrieval_service, 'retrieve_chunks', return_value=[]):
                response = await agent_service.process_query(query_request)

                assert isinstance(response, QueryResponse)
                assert response.answer == "I don't know based on the provided text."
                assert len(response.citations) == 0

    @pytest.mark.asyncio
    async def test_process_query_with_user_selected_text(self, agent_service):
        """Test that the agent processes queries with user-selected text context"""
        query_request = QueryRequest(query="Explain this concept?", context="User selected text about the concept")

        with patch.object(agent_service.llm_service, 'generate_response', return_value="The concept means..."):
            with patch.object(agent_service.retrieval_service, 'retrieve_chunks', return_value=[]):  # No Qdrant chunks
             with patch.object(GroundingService, 'validate_response', return_value=True):
                with patch.object(CitationService, 'generate_citations', return_value=["user_selected_source"]):
                    response = await agent_service.process_query(query_request)

                    assert isinstance(response, QueryResponse)
                    assert "concept" in response.answer.lower()
                    assert len(response.citations) > 0

    def test_agent_initialization(self, agent_service):
        """Test that the agent service initializes correctly"""
        assert hasattr(agent_service, 'llm_service')
        assert hasattr(agent_service, 'retrieval_service')
        assert hasattr(agent_service, 'grounding_service')
        assert hasattr(agent_service, 'citation_service')