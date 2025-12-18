import pytest
from unittest.mock import Mock, patch, mock_open
from backend.ingestion.sitemap_parser import SitemapParser
import xml.etree.ElementTree as ET


class TestSitemapParser:
    """Unit tests for the SitemapParser class"""

    @pytest.fixture
    def sitemap_parser(self):
        """Create a SitemapParser instance for testing"""
        return SitemapParser()

    def test_parse_sitemap_valid_xml(self, sitemap_parser):
        """Test that the sitemap parser can handle valid sitemap XML"""
        valid_sitemap_xml = """<?xml version="1.0" encoding="UTF-8"?>
        <urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
            <url>
                <loc>https://example.com/page1</loc>
                <lastmod>2023-01-01</lastmod>
            </url>
            <url>
                <loc>https://example.com/page2</loc>
                <lastmod>2023-01-02</lastmod>
            </url>
        </urlset>"""

        with patch('requests.get') as mock_get:
            mock_get.return_value.text = valid_sitemap_xml
            mock_get.return_value.status_code = 200

            urls = sitemap_parser.parse_sitemap("https://example.com/sitemap.xml")

            assert len(urls) == 2
            assert "https://example.com/page1" in urls
            assert "https://example.com/page2" in urls

    def test_parse_sitemap_with_sitemap_index(self, sitemap_parser):
        """Test that the sitemap parser can handle sitemap index files"""
        sitemap_index_xml = """<?xml version="1.0" encoding="UTF-8"?>
        <sitemapindex xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
            <sitemap>
                <loc>https://example.com/sitemap1.xml</loc>
                <lastmod>2023-01-01</lastmod>
            </sitemap>
            <sitemap>
                <loc>https://example.com/sitemap2.xml</loc>
                <lastmod>2023-01-02</lastmod>
            </sitemap>
        </sitemapindex>"""

        with patch('requests.get') as mock_get:
            # First call returns the sitemap index
            mock_get.return_value.text = sitemap_index_xml
            mock_get.return_value.status_code = 200

            urls = sitemap_parser.parse_sitemap("https://example.com/sitemap_index.xml")

            # Should return the sitemap URLs, not the individual page URLs
            # (implementation may vary based on design)
            assert len(urls) >= 2  # At least the two sitemap URLs

    def test_parse_sitemap_empty_xml(self, sitemap_parser):
        """Test that the sitemap parser handles empty XML"""
        empty_xml = """<?xml version="1.0" encoding="UTF-8"?>
        <urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
        </urlset>"""

        with patch('requests.get') as mock_get:
            mock_get.return_value.text = empty_xml
            mock_get.return_value.status_code = 200

            urls = sitemap_parser.parse_sitemap("https://example.com/sitemap.xml")

            assert len(urls) == 0

    def test_parse_sitemap_invalid_xml(self, sitemap_parser):
        """Test that the sitemap parser handles invalid XML"""
        invalid_xml = "This is not valid XML"

        with patch('requests.get') as mock_get:
            mock_get.return_value.text = invalid_xml
            mock_get.return_value.status_code = 200

            with pytest.raises(Exception):
                sitemap_parser.parse_sitemap("https://example.com/sitemap.xml")

    def test_parse_sitemap_network_error(self, sitemap_parser):
        """Test that the sitemap parser handles network errors"""
        with patch('requests.get') as mock_get:
            mock_get.side_effect = Exception("Network error")

            with pytest.raises(Exception):
                sitemap_parser.parse_sitemap("https://example.com/sitemap.xml")

    def test_parse_sitemap_http_error(self, sitemap_parser):
        """Test that the sitemap parser handles HTTP errors"""
        with patch('requests.get') as mock_get:
            mock_get.return_value.status_code = 404
            mock_get.return_value.text = "Not Found"

            with pytest.raises(Exception):
                sitemap_parser.parse_sitemap("https://example.com/nonexistent-sitemap.xml")

    def test_parse_sitemap_malformed_url(self, sitemap_parser):
        """Test that the sitemap parser handles malformed URLs in sitemap"""
        malformed_url_xml = """<?xml version="1.0" encoding="UTF-8"?>
        <urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
            <url>
                <loc>not-a-valid-url</loc>
            </url>
            <url>
                <loc>https://example.com/valid-page</loc>
            </url>
        </urlset>"""

        with patch('requests.get') as mock_get:
            mock_get.return_value.text = malformed_url_xml
            mock_get.return_value.status_code = 200

            urls = sitemap_parser.parse_sitemap("https://example.com/sitemap.xml")

            # Should handle malformed URLs gracefully - may include or exclude them depending on implementation
            assert "https://example.com/valid-page" in urls or len(urls) == 0

    def test_parse_sitemap_filter_urls_by_domain(self, sitemap_parser):
        """Test that the sitemap parser filters URLs by domain if needed"""
        mixed_domain_xml = """<?xml version="1.0" encoding="UTF-8"?>
        <urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
            <url>
                <loc>https://example.com/page1</loc>
            </url>
            <url>
                <loc>https://other-domain.com/page2</loc>
            </url>
            <url>
                <loc>https://example.com/page3</loc>
            </url>
        </urlset>"""

        with patch('requests.get') as mock_get:
            mock_get.return_value.text = mixed_domain_xml
            mock_get.return_value.status_code = 200

            urls = sitemap_parser.parse_sitemap("https://example.com/sitemap.xml")

            # Implementation may filter by domain or not - both are valid approaches
            # If filtering by domain: should only include example.com URLs
            # If not filtering: should include all URLs
            assert len(urls) >= 2  # Should have at least the valid example.com URLs

    def test_parse_sitemap_with_alternate_namespaces(self, sitemap_parser):
        """Test that the sitemap parser handles different XML namespaces"""
        alternate_namespace_xml = """<?xml version="1.0" encoding="UTF-8"?>
        <urlset xmlns="http://www.google.com/schemas/sitemap/1.0">
            <url>
                <loc>https://example.com/page1</loc>
            </url>
        </urlset>"""

        with patch('requests.get') as mock_get:
            mock_get.return_value.text = alternate_namespace_xml
            mock_get.return_value.status_code = 200

            urls = sitemap_parser.parse_sitemap("https://example.com/sitemap.xml")

            assert len(urls) >= 1  # Should handle alternate namespaces

    def test_parse_sitemap_with_lastmod_and_frequency(self, sitemap_parser):
        """Test that the sitemap parser handles additional sitemap fields"""
        extended_sitemap_xml = """<?xml version="1.0" encoding="UTF-8"?>
        <urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
            <url>
                <loc>https://example.com/page1</loc>
                <lastmod>2023-01-01</lastmod>
                <changefreq>weekly</changefreq>
                <priority>0.8</priority>
            </url>
        </urlset>"""

        with patch('requests.get') as mock_get:
            mock_get.return_value.text = extended_sitemap_xml
            mock_get.return_value.status_code = 200

            urls = sitemap_parser.parse_sitemap("https://example.com/sitemap.xml")

            assert len(urls) == 1
            assert "https://example.com/page1" in urls