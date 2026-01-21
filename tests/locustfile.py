"""
Locust performance testing for GUDLFT application

Run with: locust -f locustfile.py --host=http://127.0.0.1:5000
Access dashboard at: http://localhost:8089

Performance requirements:
- Data loading: < 5 seconds
- Booking updates: < 2 seconds
- Simulate 6 concurrent users
"""

from locust import HttpUser, task, between


class GUDLFTUser(HttpUser):
    """Simulates a user interacting with the GUDLFT application"""

    # Wait between 1 and 3 seconds between tasks
    wait_time = between(1, 3)

    def on_start(self):
        """Called when a simulated user starts"""
        # Valid test data
        self.email = "john@simplylift.co"
        self.club_name = "Simply Lift"
        self.competition_name = "Spring Festival"

    @task(3)
    def load_homepage(self):
        """
        Test: Load homepage with clubs points table
        Requirement: < 5 seconds
        Weight: 3 (executed 3x more often)
        """
        with self.client.get("/", catch_response=True) as response:
            if response.elapsed.total_seconds() > 5:
                response.failure(
                    f"Homepage took {response.elapsed.total_seconds():.2f}s (> 5s)"
                )
            elif response.status_code == 200:
                response.success()

    @task(2)
    def login_and_view_competitions(self):
        """
        Test: Login and load competitions list
        Requirement: < 5 seconds
        Weight: 2
        """
        with self.client.post(
            "/showSummary", data={"email": self.email}, catch_response=True
        ) as response:
            if response.elapsed.total_seconds() > 5:
                response.failure(
                    f"Login took {response.elapsed.total_seconds():.2f}s (> 5s)"
                )
            elif response.status_code == 200 and b"Welcome" in response.content:
                response.success()
            else:
                response.failure("Login failed")

    @task(1)
    def book_competition(self):
        """
        Test: Access booking page
        Requirement: < 2 seconds
        Weight: 1
        """
        with self.client.get(
            f"/book/{self.competition_name}/{self.club_name}", catch_response=True
        ) as response:
            if response.elapsed.total_seconds() > 2:
                response.failure(
                    f"Booking page took {response.elapsed.total_seconds():.2f}s (> 2s)"
                )
            elif response.status_code == 200:
                response.success()

    @task(1)
    def purchase_places(self):
        """
        Test: Submit booking (update operation)
        Requirement: < 2 seconds
        Weight: 1
        """
        with self.client.post(
            "/purchasePlaces",
            data={
                "competition": self.competition_name,
                "club": self.club_name,
                "places": "1",
            },
            catch_response=True,
        ) as response:
            if response.elapsed.total_seconds() > 2:
                response.failure(
                    f"Purchase took {response.elapsed.total_seconds():.2f}s (> 2s)"
                )
            elif response.status_code == 200:
                response.success()

    @task(1)
    def view_points_board(self):
        """
        Test: View points display board (via homepage)
        Requirement: < 5 seconds
        Weight: 1
        Note: Points are displayed on the index page
        """
        with self.client.get("/", catch_response=True) as response:
            if response.elapsed.total_seconds() > 5:
                response.failure(
                    f"Points board took {response.elapsed.total_seconds():.2f}s (> 5s)"
                )
            elif response.status_code == 200 and b"Points" in response.content:
                response.success()
            else:
                response.failure("Points board not displayed correctly")
