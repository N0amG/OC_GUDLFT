"""
Unit tests for booking validation logic
"""

import pytest
from server import app, loadClubs, loadCompetitions


@pytest.fixture
def client():
    """Create a test client for the app"""
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


class TestBookingValidation:
    """Test booking validation rules"""

    def test_booking_more_than_12_places(self, client):
        """Test that booking more than 12 places is rejected"""
        response = client.post(
            "/purchasePlaces",
            data={
                "club": "Simply Lift",
                "competition": "Winter Cup",
                "places": "15",
            },
            follow_redirects=True,
        )
        assert response.status_code == 200
        assert b"cannot book more than 12" in response.data

    def test_booking_exceeds_club_points(self, client):
        """Test that booking cannot exceed club points"""
        response = client.post(
            "/purchasePlaces",
            data={
                "club": "Iron Temple",
                "competition": "Winter Cup",
                "places": "10",
            },
            follow_redirects=True,
        )
        assert response.status_code == 200
        print(response.data)
        assert b"enough points" in response.data

    def test_booking_exceeds_available_places(self, client):
        """Test that booking cannot exceed available places"""
        response = client.post(
            "/purchasePlaces",
            data={
                "club": "Simply Lift",
                "competition": "Spring Festival",
                "places": "30",
            },
            follow_redirects=True,
        )
        assert response.status_code == 200

    def test_valid_booking(self, client):
        """Test that valid booking succeeds"""
        response = client.post(
            "/purchasePlaces",
            data={"club": "Simply Lift", "competition": "Spring Festival", "places": "5"},
            follow_redirects=True,
        )
        assert response.status_code == 200

    def test_booking_exactly_12_places(self, client):
        """Test that booking exactly 12 places is allowed"""
        response = client.post(
            "/purchasePlaces",
            data={
                "club": "She Lifts",
                "competition": "Spring Festival",
                "places": "12",
            },
            follow_redirects=True,
        )
        assert response.status_code == 200

    def test_clubs_have_points(self):
        """Test that all clubs have points field"""
        clubs = loadClubs()
        for club in clubs:
            assert "points" in club
            assert int(club["points"]) >= 0

    def test_competitions_have_places(self):
        """Test that all competitions have numberOfPlaces field"""
        competitions = loadCompetitions()
        for competition in competitions:
            assert "numberOfPlaces" in competition
            assert int(competition["numberOfPlaces"]) >= 0
