"""
Content extractor for extracting text content from web pages
"""
import requests
from typing import Dict, Optional, List
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup
import logging

logger = logging.getLogger(__name__)

class ContentExtractor:
    def __init__(self):
        pass

    async def extract_content(self, url: str) -> Optional[Dict[str, str]]:
        """
        Extract content from a given URL
        """
        try:
            logger.info(f"Extracting content from: {url}")

            # Fetch the content
            headers = {
                'User-Agent': 'Mozilla/5.0 (compatible; RAG-Chatbot-Bot/1.0; +http://example.com/bot)'
            }
            response = requests.get(url, headers=headers, timeout=30)
            response.raise_for_status()

            # Parse the HTML
            soup = BeautifulSoup(response.content, 'html.parser')

            # Remove script and style elements
            for script in soup(["script", "style"]):
                script.decompose()

            # Extract title
            title_tag = soup.find('title')
            title = title_tag.get_text().strip() if title_tag else ""

            # Extract main content - try different selectors for main content
            main_content = None

            # Try common selectors for main content
            selectors = [
                'main',
                'article',
                '[role="main"]',
                '.content',
                '.main-content',
                '.post-content',
                '.entry-content',
                'body'
            ]

            for selector in selectors:
                main_content = soup.select_one(selector)
                if main_content:
                    break

            # If no main content found, use the body
            if not main_content:
                main_content = soup.find('body')

            if main_content:
                # Extract text content, removing extra whitespace
                text_content = main_content.get_text(separator=' ', strip=True)
                # Clean up multiple spaces
                import re
                text_content = re.sub(r'\s+', ' ', text_content)
            else:
                text_content = ""

            # Extract URL parts for module/chapter info
            parsed_url = urlparse(url)
            path_parts = parsed_url.path.strip('/').split('/')

            module = path_parts[0] if path_parts and path_parts[0] else "General"
            chapter = path_parts[1] if len(path_parts) > 1 else title if title else "Chapter"

            content_data = {
                "url": url,
                "title": title,
                "content": text_content,
                "module": module,
                "chapter": chapter,
                "anchor": parsed_url.fragment
            }

            logger.info(f"Successfully extracted content from {url} ({len(text_content)} characters)")
            return content_data

        except requests.RequestException as e:
            logger.error(f"Error fetching content from {url}: {e}")
            return None
        except Exception as e:
            logger.error(f"Error extracting content from {url}: {e}")
            return None

    async def extract_content_batch(self, urls: List[str]) -> List[Dict[str, str]]:
        """
        Extract content from a batch of URLs
        """
        results = []
        for url in urls:
            content = await self.extract_content(url)
            if content:
                results.append(content)

        return results