"""
Test script to validate that RAG endpoints remain accessible to anonymous users.
This ensures that authentication doesn't block core functionality.
"""
import asyncio
import httpx
import pytest
import sys
import os
# Add the app directory to the path so we can import from it
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'app'))

from fastapi.testclient import TestClient
from app.main import app

def test_rag_endpoints_accessible_anonymously():
    """Test that RAG endpoints are accessible without authentication"""
    client = TestClient(app)

    # Test /api/v1/query endpoint without authentication
    response = client.post("/api/v1/query", json={"query": "test query"})
    # Should not return 401 (unauthorized) - might return 400 due to missing required fields
    # but should not be blocked by auth middleware
    assert response.status_code != 401, f"Query endpoint blocked for anonymous users: {response.status_code}"

    # Test /api/v1/select endpoint without authentication
    response = client.post("/api/v1/select", json={"query": "test query"})
    # Should not return 401 (unauthorized)
    assert response.status_code != 401, f"Select endpoint blocked for anonymous users: {response.status_code}"

    print("✓ RAG endpoints are accessible to anonymous users")

def test_auth_endpoints_require_authentication():
    """Test that auth endpoints properly require authentication"""
    client = TestClient(app)

    # Try to access profile endpoint without authentication
    response = client.get("/api/v1/profile")
    # Should return 401 (unauthorized) since profile requires auth
    assert response.status_code == 401, f"Profile endpoint should require authentication: {response.status_code}"

    print("✓ Auth-protected endpoints properly require authentication")

if __name__ == "__main__":
    test_rag_endpoints_accessible_anonymously()
    test_auth_endpoints_require_authentication()
    print("✓ All accessibility tests passed!")