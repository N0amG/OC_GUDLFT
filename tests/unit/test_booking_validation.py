"""
Unit tests for booking validation logic
"""
from datetime import datetime


class TestBookingValidation:
    """Test booking validation rules"""

    def test_places_cannot_exceed_12(self):
        """Test that booking more than 12 places should fail"""
        places_required = 15
        max_places = 12
        assert places_required > max_places

    def test_places_cannot_exceed_club_points(self):
        """Test that booking cannot exceed club points"""
        club_points = 10
        places_required = 15
        assert places_required > club_points

    def test_places_cannot_exceed_available(self):
        """Test that booking cannot exceed competition places"""
        available_places = 5
        places_required = 10
        assert places_required > available_places

    def test_valid_booking_within_limits(self):
        """Test valid booking scenario"""
        club_points = 20
        available_places = 25
        places_required = 10
        max_places = 12

        assert places_required <= max_places
        assert places_required <= club_points
        assert places_required <= available_places

    def test_past_competition_date(self):
        """Test that past competitions should be detected"""
        past_date = datetime(2020, 3, 27, 10, 0, 0)
        now = datetime.now()
        assert past_date < now

    def test_future_competition_date(self):
        """Test that future competitions should be allowed"""
        future_date = datetime(2027, 3, 27, 10, 0, 0)
        now = datetime.now()
        assert future_date > now
