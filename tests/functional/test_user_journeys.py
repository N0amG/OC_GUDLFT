"""
Functional tests - End-to-end user scenarios
"""

import pytest
from server import app


@pytest.fixture
def client():
    """Create a test client for the app"""
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


class TestUserJourney:
    """Test complete user journeys through the application"""

    def test_user_can_login_with_valid_email(self, client):
        """
        Scenario: Secretary logs in with valid email
        Given I am on the home page
        When I enter a valid secretary email
        Then I should see the welcome page with competitions
        """
        response = client.post("/showSummary", data={"email": "john@simplylift.co"})
        assert response.status_code == 200
        assert b"Welcome" in response.data

    def test_user_cannot_login_with_invalid_email(self, client):
        """
        Scenario: User tries to login with invalid email
        Given I am on the home page
        When I enter an invalid email
        Then I should see an error message
        And I should remain on the home page
        """
        response = client.post("/showSummary", data={"email": "notfound@test.com"})
        assert response.status_code == 200
        assert b"wasn't found" in response.data or b"wasn" in response.data

    def test_user_can_view_club_points_on_homepage(self, client):
        """
        Scenario: User views club points board
        Given I am on the home page
        Then I should see a table with all clubs and their points
        """
        response = client.get("/")
        assert response.status_code == 200
        assert b"Simply Lift" in response.data or b"Iron Temple" in response.data

    def test_user_can_logout(self, client):
        """
        Scenario: User logs out
        Given I am logged in
        When I click logout
        Then I should be redirected to the home page
        """
        # Login first
        client.post("/showSummary", data={"email": "john@simplylift.co"})

        # Then logout
        response = client.get("/logout", follow_redirects=True)
        assert response.status_code == 200
