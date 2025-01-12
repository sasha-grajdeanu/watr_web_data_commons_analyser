import requests
import time

class URLFetcher:
    """
    This class fetches data from URLs with retry logic
    """
    def __init__(self, max_retries=5, initial_delay=1):
        self.max_retries = max_retries
        self.initial_delay = initial_delay

    def fetch_with_retries(self, session, url):
        """
        Thi Function fetches N-Quads data from a URL with retries
        """
        delay = self.initial_delay
        for attempt in range(self.max_retries):
            try:
                response = session.get(url, timeout=10)
                if response.status_code == 200:
                    return response.text
                else:
                    print(f"Unexpected response for {url}. Status: {response.status_code}")
            except requests.exceptions.RequestException as e:
                print(f"Error fetching {url} (Attempt {attempt + 1}/{self.max_retries}): {e}")

            if attempt < self.max_retries - 1:
                print(f"Retrying in {delay} seconds...")
                time.sleep(delay)
                delay *= 2  # Exponential backoff (this prevents overloading the server)

        print(f"Failed to fetch {url} after {self.max_retries} attempts.")
        return None