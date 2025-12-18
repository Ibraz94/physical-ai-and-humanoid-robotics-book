"""
Gemini LLM integration service
"""
import google.generativeai as genai
from typing import List, Optional
from ..config import settings
import logging

logger = logging.getLogger(__name__)

class GeminiService:
    def __init__(self):
        # Configure the Gemini API key
        genai.configure(api_key=settings.gemini_api_key)

        # Initialize the model
        self.model = genai.GenerativeModel(settings.gemini_model)

    async def generate_response(self, query: str, context_chunks: List[str]) -> str:
        """
        Generate a response using Gemini based on the query and context
        """
        try:
            # Combine context chunks into a single context string
            context_str = "\n\n".join(context_chunks)

            # Create the prompt with strict grounding rules
            prompt = f"""
            You are a helpful assistant that answers questions based only on the provided context.

            Context:
            {context_str}

            Question: {query}

            Instructions:
            - Answer the question based ONLY on the provided context
            - If the context does not contain sufficient information to answer the question, respond with: "I don't know based on the provided text."
            - Do not use any external knowledge, browsing, or hallucinations
            - Be concise and accurate
            - Include relevant information from the context in your response
            """

            # Generate content using Gemini
            # Note: The Google Generative AI Python SDK doesn't have a true async method
            # So we'll use the sync version in an executor to make it awaitable
            import asyncio
            loop = asyncio.get_event_loop()
            response = await loop.run_in_executor(None, lambda: self.model.generate_content(prompt))

            # Extract the text response
            answer = response.text.strip() if response.text else ""

            # Validate the response to ensure it follows grounding rules
            if not answer or "I don't know based on the provided text." not in answer and len(answer) < 5:
                logger.warning("Generated response seems invalid, using default insufficient context response")
                return "I don't know based on the provided text."

            logger.info(f"Generated response with {len(answer)} characters")
            return answer

        except Exception as e:
            logger.error(f"Error generating response with Gemini: {e}")
            # Return the standard insufficient context response if there's an error
            return "I don't know based on the provided text."