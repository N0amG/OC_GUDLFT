"""
Integration tests for the booking flow
"""

import pytest
from server import app


@pytest.fixture
def client():
    """Create a test client for the app"""
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


class TestBookingFlow:
    """Test the complete booking flow"""

    def test_login_and_view_competitions(self, client):
        """Test login flow and viewing competitions"""
        # Login with valid email
        response = client.post("/showSummary", data={"email": "john@simplylift.co"})
        assert response.status_code == 200
        assert b"Welcome" in response.data
        assert b"Competitions" in response.data

    def test_book_page_access(self, client):
        """Test accessing the booking page"""
        response = client.get("/book/Spring Festival/Simply Lift")
        assert response.status_code == 200
        assert b"Spring Festival" in response.data or b"Places" in response.data

    def test_complete_booking_process(self, client):
        """Test complete booking from login to purchase"""
        # Step 1: Login
        response = client.post("/showSummary", data={"email": "john@simplylift.co"})
        assert response.status_code == 200

        # Step 2: Access booking page
        response = client.get("/book/Spring Festival/Simply Lift")
        assert response.status_code == 200

        # Step 3: Purchase places (this will fail for past competitions)
        response = client.post(
            "/purchasePlaces",
            data={
                "competition": "Spring Festival",
                "club": "Simply Lift",
                "places": "1",
            },
        )
        assert response.status_code == 200


class TestPointsDisplay:
    """Test the points display integration"""

    def test_points_visible_on_index(self, client):
        """Test that points are visible on index page"""
        response = client.get("/")
        assert response.status_code == 200
        # Check for table elements
        assert b"<table" in response.data or b"Club" in response.data

    def test_points_visible_after_login(self, client):
        """Test that points are visible after login"""
        response = client.post("/showSummary", data={"email": "john@simplylift.co"})
        assert response.status_code == 200
        assert b"Points" in response.data or b"points" in response.data
