import requests
import os
from dotenv import load_dotenv

# pull API key from .env
load_dotenv()

BASE_URL = "https://trading-api.kalshi.com/trade-api/v2"

API_KEY = os.getenv("KALSHI_API_KEY")

# This sets up the communication path btwn Kalshi and our script
HEADERS = {
    "accept": "application/json",
    "Authorization": f"Token {API_KEY}"
}

