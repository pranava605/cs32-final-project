import requests
import os
import time
import base64
from dotenv import load_dotenv
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding

# pull API key from .env
load_dotenv()

BASE_URL = "https://trading-api.kalshi.com/trade-api/v2"

KEY_ID = os.getenv("KALSHI_KEY_ID")
PRIVATE_KEY_PATH = os.getenv("KALSHI_PRIVATE_KEY_PATH")

# This sets up the communication path btwn Kalshi and our script
def sign_request(method, path):
    timestamp = str(int(time.time() * 1000))
    message = timestamp + method.upper() + path
    signature = PRIVATE_KEY.sign(
        message.encode("utf-8"),
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.DIGEST_LENGTH
        ),
        hashes.SHA256()
    )
    return timestamp, base64.b64encode(signature).decode("utf-8")

def get_headers(method, path):
    timestamp, signature = sign_request(method, path)
    return {
        "accept": "application/json",
        "KALSHI-ACCESS-KEY": KEY_ID,
        "KALSHI-ACCESS-TIMESTAMP": timestamp,
        "KALSHI-ACCESS-SIGNATURE": signature
    }

def get_markets(limit=100):
    try:
        response = requests.get(
            f"{BASE_URL}/markets",
            headers = HEADERS,
            params = {"status": "open", "limit": limit}
        )
        response.raise_for_status()
        return response.json().get("markets", [])
    except requests.exceptions.ConnectionError:
        print("No internet connection.")
        return []
    except requests.exceptions.HTTPError as e:
        print(f"HTTP error: {e}")
        return []

markets = get_markets()
print(f"Found {len(markets)} markets")
print(markets[0])
