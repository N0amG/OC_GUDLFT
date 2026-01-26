"""
Unit tests for Flask routes
"""

import pytest
from server import app


@pytest.fixture
def client():
    """Create a test client for the app"""
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


class TestIndexRoute:
    """Test the index route"""

    def test_index_status_code(self, client):
        """Test that index returns 200 status code"""
        response = client.get("/")
        assert response.status_code == 200

    def test_index_contains_clubs_table(self, client):
        """Test that index page contains clubs points table"""
        response = client.get("/")
        assert b"Club Points" in response.data or b"Club Name" in response.data


class TestShowSummaryRoute:
    """Test the showSummary route"""

    def test_showSummary_valid_email(self, client):
        """Test showSummary with valid email"""
        response = client.post("/showSummary", data={"email": "john@simplylift.co"})
        assert response.status_code == 200
        assert b"Welcome" in response.data

    def test_showSummary_invalid_email(self, client):
        """Test showSummary with invalid email"""
        response = client.post("/showSummary", data={"email": "invalid@test.com"})
        assert response.status_code == 200
        assert b"email wasn't found" in response.data or b"email wasn" in response.data


class TestLogoutRoute:
    """Test the logout route"""

    def test_logout_redirects(self, client):
        """Test that logout redirects to index"""
        response = client.get("/logout")
        assert response.status_code == 302  # Redirect status
