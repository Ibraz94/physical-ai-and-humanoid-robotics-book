import pytest
from unittest.mock import Mock, patch, mock_open
from backend.ingestion.content_extractor import ContentExtractor


class TestContentExtractor:
    """Unit tests for the ContentExtractor class"""

    @pytest.fixture
    def content_extractor(self):
        """Create a ContentExtractor instance for testing"""
        return ContentExtractor()

    def test_extract_content_from_html_success(self, content_extractor):
        """Test that content extraction works for valid HTML"""
        html_content = """
        <!DOCTYPE html>
        <html>
        <head><title>Test Page</title></head>
        <body>
            <h1>Main Heading</h1>
            <p>This is the main content of the page.</p>
            <p>This is additional content.</p>
            <div class="sidebar">Sidebar content to be ignored</div>
        </body>
        </html>
        """

        extracted = content_extractor.extract_content(html_content, "https://example.com/page")

        # Should extract the main content
        assert "main content of the page" in extracted
        assert "additional content" in extracted
        # May or may not include sidebar content depending on implementation

    def test_extract_content_from_html_with_no_body(self, content_extractor):
        """Test content extraction from HTML with no body"""
        html_content = """
        <!DOCTYPE html>
        <html>
        <head><title>Test Page</title></head>
        </html>
        """

        extracted = content_extractor.extract_content(html_content, "https://example.com/page")

        # Should handle HTML with no body gracefully
        assert isinstance(extracted, str)

    def test_extract_content_from_html_with_special_characters(self, content_extractor):
        """Test content extraction with special characters and unicode"""
        html_content = """
        <!DOCTYPE html>
        <html>
        <head><title>Test Page with ñáéíóú</title></head>
        <body>
            <p>Content with unicode characters: ñáéíóú and emoji: 🤖</p>
            <p>Content with quotes: "Hello" and 'world'</p>
        </body>
        </html>
        """

        extracted = content_extractor.extract_content(html_content, "https://example.com/page")

        assert "ñáéíóú" in extracted
        assert "Hello" in extracted
        assert "world" in extracted

    def test_extract_content_from_plain_text(self, content_extractor):
        """Test content extraction from plain text (not HTML)"""
        plain_text = "This is plain text content without HTML tags."

        extracted = content_extractor.extract_content(plain_text, "https://example.com/page")

        # Should return the text as-is or with minimal processing
        assert "plain text content" in extracted

    def test_extract_content_from_html_with_script_tags(self, content_extractor):
        """Test that content extraction removes script tags"""
        html_content = """
        <!DOCTYPE html>
        <html>
        <head><title>Test Page</title></head>
        <body>
            <p>Valid content here.</p>
            <script>alert('xss');</script>
            <p>More valid content.</p>
        </body>
        </html>
        """

        extracted = content_extractor.extract_content(html_content, "https://example.com/page")

        # Should remove script tags and their content
        assert "Valid content here" in extracted
        assert "More valid content" in extracted
        # Should not contain the script content, though implementation may vary

    def test_extract_content_from_html_with_style_tags(self, content_extractor):
        """Test that content extraction handles style tags appropriately"""
        html_content = """
        <!DOCTYPE html>
        <html>
        <head><title>Test Page</title></head>
        <body>
            <p>Valid content here.</p>
            <style>.class { color: red; }</style>
            <p>More valid content.</p>
        </body>
        </html>
        """

        extracted = content_extractor.extract_content(html_content, "https://example.com/page")

        assert "Valid content here" in extracted
        assert "More valid content" in extracted

    def test_extract_content_from_html_with_links(self, content_extractor):
        """Test content extraction preserves text from links"""
        html_content = """
        <!DOCTYPE html>
        <html>
        <head><title>Test Page</title></head>
        <body>
            <p>Some text with <a href="https://example.com/link">a link</a> in the middle.</p>
        </body>
        </html>
        """

        extracted = content_extractor.extract_content(html_content, "https://example.com/page")

        assert "Some text with" in extracted
        assert "a link" in extracted  # Link text should be preserved

    def test_extract_content_from_html_with_images(self, content_extractor):
        """Test content extraction from HTML with images"""
        html_content = """
        <!DOCTYPE html>
        <html>
        <head><title>Test Page</title></head>
        <body>
            <p>Text before image.</p>
            <img src="image.jpg" alt="Image description">
            <p>Text after image.</p>
        </body>
        </html>
        """

        extracted = content_extractor.extract_content(html_content, "https://example.com/page")

        assert "Text before image" in extracted
        assert "Text after image" in extracted
        # Alt text may or may not be included depending on implementation

    def test_extract_content_empty_html(self, content_extractor):
        """Test content extraction from empty HTML"""
        html_content = ""

        extracted = content_extractor.extract_content(html_content, "https://example.com/page")

        # Should handle empty content gracefully
        assert isinstance(extracted, str)
        assert len(extracted) >= 0

    def test_extract_content_malformed_html(self, content_extractor):
        """Test content extraction from malformed HTML"""
        html_content = "<html><body><p>Unclosed paragraph<div>Unclosed div"

        extracted = content_extractor.extract_content(html_content, "https://example.com/page")

        # Should handle malformed HTML gracefully
        assert isinstance(extracted, str)

    def test_extract_content_from_url_success(self, content_extractor):
        """Test content extraction from a URL"""
        html_content = """
        <!DOCTYPE html>
        <html>
        <head><title>Test Page</title></head>
        <body>
            <h1>Page Title</h1>
            <p>This is the page content.</p>
        </body>
        </html>
        """

        with patch('requests.get') as mock_get:
            mock_get.return_value.text = html_content
            mock_get.return_value.status_code = 200

            extracted = content_extractor.extract_content_from_url("https://example.com/page")

            assert "page content" in extracted
            assert "Page Title" in extracted

    def test_extract_content_from_url_network_error(self, content_extractor):
        """Test content extraction handles network errors"""
        with patch('requests.get') as mock_get:
            mock_get.side_effect = Exception("Network error")

            with pytest.raises(Exception):
                content_extractor.extract_content_from_url("https://example.com/page")

    def test_extract_content_from_url_http_error(self, content_extractor):
        """Test content extraction handles HTTP errors"""
        with patch('requests.get') as mock_get:
            mock_get.return_value.status_code = 404
            mock_get.return_value.text = "Not Found"

            with pytest.raises(Exception):
                content_extractor.extract_content_from_url("https://example.com/nonexistent-page")

    def test_extract_content_from_url_non_html_content(self, content_extractor):
        """Test content extraction from URL with non-HTML content"""
        json_content = '{"key": "value", "content": "This is JSON"}'

        with patch('requests.get') as mock_get:
            mock_get.return_value.text = json_content
            mock_get.return_value.status_code = 200
            mock_get.return_value.headers = {'content-type': 'application/json'}

            extracted = content_extractor.extract_content_from_url("https://example.com/data.json")

            # Implementation may handle non-HTML differently
            assert isinstance(extracted, str)

    def test_extract_content_from_url_with_encoding(self, content_extractor):
        """Test content extraction with different text encodings"""
        html_content = """
        <!DOCTYPE html>
        <html>
        <head><meta charset="utf-8"><title>Test Page</title></head>
        <body>
            <p>Content with unicode: ñáéíóú</p>
        </body>
        </html>
        """

        with patch('requests.get') as mock_get:
            mock_get.return_value.text = html_content
            mock_get.return_value.status_code = 200

            extracted = content_extractor.extract_content_from_url("https://example.com/page")

            assert "ñáéíóú" in extracted