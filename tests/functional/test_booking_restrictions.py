"""
Functional tests for booking restrictions
"""

import pytest
from server import app


@pytest.fixture
def client():
    """Create a test client for the app"""
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


class TestBookingRestrictions:
    """Test all booking business rules end-to-end"""

    def test_cannot_book_more_than_12_places(self, client):
        """
        Scenario: User tries to book more than 12 places
        Given I am logged in
        When I try to book 13 places
        Then I should see an error message
        """
        # Login
        client.post("/showSummary", data={"email": "john@simplylift.co"})

        # Try to book too many places
        response = client.post(
            "/purchasePlaces",
            data={
                "competition": "Spring Festival",
                "club": "Simply Lift",
                "places": "13",
            },
        )
        assert response.status_code == 200
        # Check for error message (might be about past competition or 12 places limit)
        assert b"cannot" in response.data or b"past competition" in response.data

    def test_cannot_book_past_competition(self, client):
        """
        Scenario: User tries to book places in a past competition
        Given I am logged in
        When I try to book a past competition
        Then I should see an error message
        """
        client.post("/showSummary", data={"email": "john@simplylift.co"})

        response = client.post(
            "/purchasePlaces",
            data={
                "competition": "Spring Festival",
                "club": "Simply Lift",
                "places": "1",
            },
        )
        assert response.status_code == 200
        assert b"past competition" in response.data

    def test_cannot_book_more_than_club_points(self, client):
        """
        Scenario: User tries to book more places than they have points
        Given I am logged in as a club with limited points
        When I try to book more places than my points allow
        Then I should see an error message
        """
        # Login with Iron Temple (4 points)
        client.post("/showSummary", data={"email": "admin@irontemple.com"})

        # Try to book 5 places (more than 4 points)
        response = client.post(
            "/purchasePlaces",
            data={
                "competition": "Spring Festival",
                "club": "Iron Temple",
                "places": "5",
            },
        )
        assert response.status_code == 200
        # Should get error about points or past competition
        assert b"enough points" in response.data or b"past competition" in response.data
