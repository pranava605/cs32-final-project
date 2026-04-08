import pandas as pd
from kalshi_client import get_markets

def most_contested_markets(n=10):
    # get the live markets from Kalshi
    markets = get_markets()
    if not markets:
        return pd.DataFrame()

    contested = []

    for market in markets:
        # get the relevant data fields needed

        yes_ask = market.get("yes_ask_dollars")
        no_bid = market.get("no_bid_dollars")

        ticker = market.get("ticker")
        title = market.get("title", "Unknown")
        volume = market.get("volume_fp")

        # don't consider markets without price data
        if yes_ask is None:
            continue

        # makes sure yes_ask is a number not a string
        yes_ask = float(yes_ask)

        if not ticker.startswith("KXNBA"):
            continue

        if "20+" not in title and "25+" not in title:
            continue

        # closer to 0.5 the more contested the outcome
        distance_from_50 = abs(yes_ask - 0.50)

        contested.append({
            "ticker": ticker,
            "title": title,
            "yes_ask": yes_ask,
            "no_bid": no_bid,
            "volume": volume,
            "distance_from_50": round(distance_from_50, 4)})

    # sort by markets closest to 50/50 probabilities
    df = pd.DataFrame(contested)
    df = df.sort_values("distance_from_50", ascending=True)
    return df.head(n)

if __name__ == "__main__":
    df = most_contested_markets()
    if not df.empty:
        for i, row in df.iterrows():
            print(f"\n{'='*50}")
            print(f"  MARKET {i+1}")
            print(f"{'='*50}")
            print(f"  Ticker:  {row['ticker']}")
            print(f"  Title:   {row['title']}")

            # display prices in cents and multiply by 100. note that the float makes sure they are numbers
            print(f"  Yes Ask: {float(row['yes_ask'])*100:.0f}c  |  No Bid: {float(row['no_bid'])*100:.0f}c")
            print(f"  Volume:  {row['volume']}")
            print(f"  Distance from 50/50: {row['distance_from_50']*100}c")
