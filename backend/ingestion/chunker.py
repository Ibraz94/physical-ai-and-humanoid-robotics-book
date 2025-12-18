"""
Content chunker for splitting content into 400-700 token chunks with overlap
"""
import re
from typing import List, Dict, Any
import logging

logger = logging.getLogger(__name__)

class ContentChunker:
    def __init__(self, min_tokens: int = 400, max_tokens: int = 700, overlap_ratio: float = 0.2):
        self.min_tokens = min_tokens
        self.max_tokens = max_tokens
        self.overlap_ratio = overlap_ratio

    def count_tokens(self, text: str) -> int:
        """
        Count the number of tokens in a text (simple approximation using words)
        """
        if not text:
            return 0
        # Simple tokenization based on words (in a real implementation, you'd use a proper tokenizer)
        # This is a rough approximation - 1 word ~ 1 token
        words = re.findall(r'\b\w+\b', text.lower())
        return len(words)

    def chunk_content(self, content_data: Dict[str, str]) -> List[Dict[str, Any]]:
        """
        Chunk the content into 400-700 token pieces with overlap
        """
        try:
            url = content_data["url"]
            title = content_data["title"]
            full_content = content_data["content"]
            module = content_data["module"]
            chapter = content_data["chapter"]
            anchor = content_data["anchor"]

            # Validate content integrity
            if not self._validate_content_integrity(full_content):
                logger.warning(f"Content integrity check failed for {url}")
                return []

            logger.info(f"Chunking content from {url} ({self.count_tokens(full_content)} tokens)")

            # Split content into sentences to maintain semantic boundaries
            sentences = re.split(r'[.!?]+\s+', full_content)

            chunks = []
            current_chunk = ""
            current_tokens = 0
            chunk_idx = 0

            for sentence in sentences:
                sentence_tokens = self.count_tokens(sentence)

                # If adding this sentence would exceed max tokens
                if current_tokens + sentence_tokens > self.max_tokens and current_chunk:
                    # Save the current chunk if it meets minimum size requirements
                    if current_tokens >= self.min_tokens:
                        chunk_id = f"{url.replace('://', '_').replace('/', '_')}_{chunk_idx}"
                        chunk = {
                            "chunk_id": chunk_id,
                            "content": current_chunk.strip(),
                            "source_url": url,
                            "title": title,
                            "module": module,
                            "chapter": chapter,
                            "anchor": anchor,
                            "token_count": current_tokens
                        }
                        chunks.append(chunk)
                        chunk_idx += 1

                        # Apply overlap: keep the last portion of the current chunk
                        overlap_tokens = int(self.max_tokens * self.overlap_ratio)
                        # Find the overlap content by counting backwards
                        current_chunk, current_tokens = self._get_overlap_content(current_chunk, overlap_tokens)
                    else:
                        # If current chunk is too small, try to add the sentence anyway
                        current_chunk += " " + sentence
                        current_tokens += sentence_tokens
                else:
                    # Add sentence to current chunk
                    current_chunk += " " + sentence
                    current_tokens += sentence_tokens

            # Add the last chunk if it has content
            if current_chunk.strip() and current_tokens >= self.min_tokens:
                chunk_id = f"{url.replace('://', '_').replace('/', '_')}_{chunk_idx}"
                chunk = {
                    "chunk_id": chunk_id,
                    "content": current_chunk.strip(),
                    "source_url": url,
                    "title": title,
                    "module": module,
                    "chapter": chapter,
                    "anchor": anchor,
                    "token_count": current_tokens
                }
                chunks.append(chunk)

            logger.info(f"Created {len(chunks)} chunks from content")
            return chunks

        except Exception as e:
            logger.error(f"Error chunking content: {e}")
            return []

    def _validate_content_integrity(self, content: str) -> bool:
        """
        Validate content integrity to ensure it's not corrupted or malformed
        """
        try:
            if not content:
                return False

            # Check for common corruption indicators
            if len(content) < 10:  # Too short to be meaningful content
                return False

            # Check for excessive special characters that might indicate corruption
            special_char_ratio = len([c for c in content if not c.isalnum() and not c.isspace()]) / len(content)
            if special_char_ratio > 0.5:  # More than 50% special characters
                logger.warning("Content has excessive special characters")
                return False

            # Check for common encoding issues
            if '' in content:  # Replacement character often indicates encoding issues
                logger.warning("Content contains replacement characters indicating encoding issues")
                return False

            # Check for null bytes or other control characters
            if '\x00' in content:
                logger.warning("Content contains null bytes")
                return False

            return True

        except Exception as e:
            logger.error(f"Error validating content integrity: {e}")
            return False

    def _get_overlap_content(self, chunk: str, target_tokens: int) -> tuple[str, int]:
        """
        Extract the end portion of a chunk that contains approximately target_tokens
        """
        words = chunk.split()
        current_tokens = 0
        overlap_words = []

        # Start from the end and work backwards
        for word in reversed(words):
            word_tokens = self.count_tokens(word)
            if current_tokens + word_tokens <= target_tokens:
                overlap_words.insert(0, word)  # Insert at the beginning to maintain order
                current_tokens += word_tokens
            else:
                break

        return " ".join(overlap_words), current_tokens