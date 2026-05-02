import requests

kalshi_url = "https://api.elections.kalshi.com/trade-api/v2"


# First send a request to the Kalshi API'''

def kalshi_request(url_ending, specifics=None):
# url ending is added to the url to help get us specific game data
# parameters help with if we need to specify which markets

# first get full url based on the ending
    final_url = kalshi_url + url_ending

    # send the request to the api
    # requests.get connects us to the api, gets us the data
    # specifics helps with the number of markets
    
    # AI added a try/except to our existing .get() to prevent http request errors
    try:
        api_info = requests.get(final_url, params=specifics, timeout=10)
        api_info.raise_for_status()
    except requests.RequestException as e:
        print(f"Kalshi request failed: {e}")
        return {}

    # need to convert the api's info into data we can use in python
    api_data = api_info.json()

    return api_data

def trump_markets():
    markets = []
    # we are trying to store all the trump markets from kalshi

    next_cursor = None
    # keeps track of which page of data we're on
    # None means we are starting at the beginning

    while True:
        # we want to keep going until we have all pages
        specifics_data = {
        "status": "open",
        "limit": 100,
        # gets us 100 events at a time, so one page
        
        # line below added by AI to make kalshi/markets request more efficient
        "with_nested_markets": "true"

        # ask kalshi to return each event's markets inline so we don't need a second call per event
        }
        if next_cursor is not None:
            specifics_data["cursor"] = next_cursor

        # Basically, we are sending the cursor to Kalshi to request the next page. 
        # Kalshi gives us back a new cursor for the next page (from our kalshi_data variable),
        # and we keep going with this until we’ve gone through all the data.


        kalshi_data = kalshi_request("/events", specifics_data)
        # kalshi_data is a dictionary with all the returned info, but this has a lot of info

        # we  want the list of events on the page
        events_list = kalshi_data.get("events", [])

        # events list only has one page of data, so we need to add them all to the overall list by looping through each events markets
        for event in events_list:
            event_ticker = event.get("event_ticker", "")
            if "TRUMP" in event_ticker.upper():
            # if event_ticker.upper().startswith("KXEL"):
                for market in event.get("markets", []):
                    markets.append(market)

        next_cursor = kalshi_data.get("cursor")

        if not next_cursor:
            break

    return markets
   

def market_prices(ticker):
    # now we want the prices for a specific market
    kalshi_data = kalshi_request(f'/markets/{ticker}', None)
    # no specifics since we are specifying a link
    # use an f string to go straight to the market using the ticker

    # ai added .get() chains so a failed kalshi_request (returns {}) or a
    # market object missing fields gives None values instead of KeyError
    market_data = kalshi_data.get("market") or {}

    return {
        "yes_ask": market_data.get("yes_ask_dollars"),
        "no_ask":  market_data.get("no_ask_dollars"),
    }
