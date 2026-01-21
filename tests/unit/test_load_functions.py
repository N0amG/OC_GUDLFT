"""
Unit tests for server.py utility functions
"""

from server import loadClubs, loadCompetitions


class TestLoadFunctions:
    """Test data loading functions"""

    def test_loadClubs_returns_list(self):
        """Test that loadClubs returns a list"""
        clubs = loadClubs()
        assert isinstance(clubs, list)

    def test_loadClubs_not_empty(self):
        """Test that loadClubs returns non-empty list"""
        clubs = loadClubs()
        assert len(clubs) > 0

    def test_loadClubs_structure(self):
        """Test that each club has required fields"""
        clubs = loadClubs()
        required_fields = ("name", "email", "points")
        for club in clubs:
            for field in required_fields:
                assert field in club

    def test_loadCompetitions_returns_list(self):
        """Test that loadCompetitions returns a list"""
        competitions = loadCompetitions()
        assert isinstance(competitions, list)

    def test_loadCompetitions_not_empty(self):
        """Test that loadCompetitions returns non-empty list"""
        competitions = loadCompetitions()
        assert len(competitions) > 0

    def test_loadCompetitions_structure(self):
        """Test that each competition has required fields"""
        competitions = loadCompetitions()
        required_fields = ("name", "date", "numberOfPlaces")
        for comp in competitions:
            for field in required_fields:
                assert field in comp
