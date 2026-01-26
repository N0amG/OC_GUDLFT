"""
Functional tests using Selenium - End-to-end browser tests
"""

import pytest
import threading
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from server import app


@pytest.fixture(scope="module")
def server():
    """Start Flask server in a background thread"""
    server_thread = threading.Thread(
        target=lambda: app.run(port=5000, use_reloader=False, debug=False)
    )
    server_thread.daemon = True
    server_thread.start()
    time.sleep(1)  # Wait for server to start
    yield
    # Server stops when thread ends


@pytest.fixture
def browser():
    """Create a Chrome browser instance"""
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  # comment to see the browser
    options.add_argument("--no-sandbox")
    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()), options=options
    )
    yield driver
    driver.quit()


class TestFunctionalSelenium:
    """Functional tests with real browser"""

    def test_complete_booking_flow(self, server, browser):
        """Test: User logs in, sees welcome, books places, points decrease"""
        import re

        # 1. Go to homepage
        browser.get("http://127.0.0.1:5000/")

        # 2. Login
        email_input = browser.find_element(By.NAME, "email")
        email_input.send_keys("john@simplylift.co")
        browser.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
        time.sleep(0.5)  # Wait for page to load

        # 3. Check welcome page
        assert "Welcome" in browser.page_source

        # 4. Get points before booking
        page_content = browser.page_source
        points_match = re.search(r"Points available:\s*(\d+)", page_content)
        assert points_match, "Could not find 'Points available' on page"
        points_before = int(points_match.group(1))

        # 5. Go to booking page for Winter Cup (future competition)
        browser.get("http://127.0.0.1:5000/book/Winter%20Cup/Simply%20Lift")

        # 6. Book 3 places
        places_input = browser.find_element(By.NAME, "places")
        places_input.clear()
        places_input.send_keys("3")
        browser.find_element(By.CSS_SELECTOR, "button[type='submit']").click()

        # 7. Check points decreased by 3
        page_content = browser.page_source
        points_match = re.search(r"Points available:\s*(\d+)", page_content)
        assert points_match, "Could not find 'Points available' after booking"
        points_after = int(points_match.group(1))
        assert points_before - 3 == points_after, f"Expected {points_before - 3} points, got {points_after}"
