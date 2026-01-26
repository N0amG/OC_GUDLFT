"""
Unit tests for server.py utility functions
Uses mocks to isolate from external dependencies (files)
"""

import json
from unittest.mock import patch, mock_open

from server import loadClubs, loadCompetitions


class TestLoadClubs:
    """Unit tests for loadClubs function with mocked file I/O"""

    def test_loadClubs_returns_list(self):
        """Test that loadClubs returns a list"""
        mock_data = json.dumps({
            "clubs": [
                {"name": "Test Club", "email": "test@test.com", "points": "10"}
            ]
        })
        with patch("builtins.open", mock_open(read_data=mock_data)):
            clubs = loadClubs()
            assert isinstance(clubs, list)

    def test_loadClubs_returns_correct_data(self):
        """Test that loadClubs returns the correct club data"""
        mock_data = json.dumps({
            "clubs": [
                {"name": "Club A", "email": "a@test.com", "points": "15"},
                {"name": "Club B", "email": "b@test.com", "points": "20"}
            ]
        })
        with patch("builtins.open", mock_open(read_data=mock_data)):
            clubs = loadClubs()
            assert len(clubs) == 2
            assert clubs[0]["name"] == "Club A"
            assert clubs[1]["points"] == "20"

    def test_loadClubs_structure(self):
        """Test that each club has required fields"""
        mock_data = json.dumps({
            "clubs": [
                {"name": "Test Club", "email": "test@test.com", "points": "10"}
            ]
        })
        with patch("builtins.open", mock_open(read_data=mock_data)):
            clubs = loadClubs()
            required_fields = ("name", "email", "points")
            for club in clubs:
                for field in required_fields:
                    assert field in club

    def test_loadClubs_empty_list(self):
        """Test that loadClubs handles empty clubs list"""
        mock_data = json.dumps({"clubs": []})
        with patch("builtins.open", mock_open(read_data=mock_data)):
            clubs = loadClubs()
            assert clubs == []

    def test_loadClubs_opens_correct_file(self):
        """Test that loadClubs opens the correct file"""
        mock_data = json.dumps({"clubs": []})
        with patch("builtins.open", mock_open(read_data=mock_data)) as mock_file:
            loadClubs()
            mock_file.assert_called_once_with("clubs.json")


class TestLoadCompetitions:
    """Unit tests for loadCompetitions function with mocked file I/O"""

    def test_loadCompetitions_returns_list(self):
        """Test that loadCompetitions returns a list"""
        mock_data = json.dumps({
            "competitions": [
                {"name": "Test Comp", "date": "2026-03-15 10:00:00", "numberOfPlaces": "25"}
            ]
        })
        with patch("builtins.open", mock_open(read_data=mock_data)):
            competitions = loadCompetitions()
            assert isinstance(competitions, list)

    def test_loadCompetitions_returns_correct_data(self):
        """Test that loadCompetitions returns the correct competition data"""
        mock_data = json.dumps({
            "competitions": [
                {"name": "Spring Cup", "date": "2026-04-01 09:00:00", "numberOfPlaces": "30"},
                {"name": "Summer Games", "date": "2026-07-15 14:00:00", "numberOfPlaces": "50"}
            ]
        })
        with patch("builtins.open", mock_open(read_data=mock_data)):
            competitions = loadCompetitions()
            assert len(competitions) == 2
            assert competitions[0]["name"] == "Spring Cup"
            assert competitions[1]["numberOfPlaces"] == "50"

    def test_loadCompetitions_structure(self):
        """Test that each competition has required fields"""
        mock_data = json.dumps({
            "competitions": [
                {"name": "Test Comp", "date": "2026-03-15 10:00:00", "numberOfPlaces": "25"}
            ]
        })
        with patch("builtins.open", mock_open(read_data=mock_data)):
            competitions = loadCompetitions()
            required_fields = ("name", "date", "numberOfPlaces")
            for comp in competitions:
                for field in required_fields:
                    assert field in comp

    def test_loadCompetitions_empty_list(self):
        """Test that loadCompetitions handles empty competitions list"""
        mock_data = json.dumps({"competitions": []})
        with patch("builtins.open", mock_open(read_data=mock_data)):
            competitions = loadCompetitions()
            assert competitions == []

    def test_loadCompetitions_opens_correct_file(self):
        """Test that loadCompetitions opens the correct file"""
        mock_data = json.dumps({"competitions": []})
        with patch("builtins.open", mock_open(read_data=mock_data)) as mock_file:
            loadCompetitions()
            mock_file.assert_called_once_with("competitions.json")
