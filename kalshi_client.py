import requests

BASE_URL = "https://api.elections.kalshi.com/trade-api/v2"

def get_markets(limit=100):
    try:
        response = requests.get(
            f"{BASE_URL}/markets",
            params={"status": "open", "limit": limit}
        )
        response.raise_for_status()
        return response.json().get("markets", [])
    except requests.exceptions.ConnectionError:
        print("No internet connection.")
        return []
    except requests.exceptions.HTTPError as e:
        print(f"HTTP error: {e}")
        return []
