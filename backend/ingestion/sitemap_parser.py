"""
Sitemap parser for extracting URLs from sitemap.xml
"""
import requests
from typing import List
from urllib.parse import urljoin, urlparse
import xml.etree.ElementTree as ET
import logging

logger = logging.getLogger(__name__)

class SitemapParser:
    def __init__(self):
        pass

    async def parse_sitemap(self, sitemap_url: str) -> List[str]:
        """
        Parse a sitemap.xml file and extract all URLs
        """
        try:
            logger.info(f"Parsing sitemap: {sitemap_url}")

            # Fetch the sitemap
            response = requests.get(sitemap_url)
            response.raise_for_status()

            # Parse the XML content
            root = ET.fromstring(response.content)

            # Handle both regular sitemaps and sitemap indexes
            urls = []
            namespace = {'ns': 'http://www.sitemaps.org/schemas/sitemap/0.9'}

            # Check if this is a sitemap index (contains sitemap elements)
            sitemap_elements = root.findall('ns:sitemap/ns:loc', namespace) or root.findall('.//ns:loc', namespace)

            if root.tag.endswith('sitemapindex'):
                # This is a sitemap index, need to fetch individual sitemaps
                for sitemap_elem in root.findall('ns:sitemap', namespace):
                    loc_elem = sitemap_elem.find('ns:loc', namespace)
                    if loc_elem is not None:
                        nested_sitemap_url = loc_elem.text.strip()
                        nested_urls = await self.parse_sitemap(nested_sitemap_url)
                        urls.extend(nested_urls)
            else:
                # This is a regular sitemap with URL entries
                for url_elem in root.findall('ns:url', namespace):
                    loc_elem = url_elem.find('ns:loc', namespace)
                    if loc_elem is not None:
                        urls.append(loc_elem.text.strip())

            logger.info(f"Extracted {len(urls)} URLs from sitemap")
            return urls

        except requests.RequestException as e:
            logger.error(f"Error fetching sitemap: {e}")
            return []
        except ET.ParseError as e:
            logger.error(f"Error parsing sitemap XML: {e}")
            return []
        except Exception as e:
            logger.error(f"Unexpected error parsing sitemap: {e}")
            return []

    async def extract_urls_from_sitemap(self, sitemap_url: str) -> List[str]:
        """
        Public method to extract URLs from a sitemap
        """
        return await self.parse_sitemap(sitemap_url)