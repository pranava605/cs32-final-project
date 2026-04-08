import pandas as pd
from kalshi_client import get_markets

def most_contested_markets(n=10):
    markets = get_markets()
    if not markets:
        print("No markets fetched.")
        return pd.DataFrame()

    contested = []

    for market in markets:
        ticker = market.get("ticker")
        title = market.get("title", "Unknown")
        yes_price = market.get("yes_ask_dollars")

        if yes_price is None:
            continue

        yes_price = float(yes_price)
        distance_from_50 = abs(yes_price - 0.50)

        contested.append({
            "ticker": ticker,
            "title": title,
            "yes_ask": yes_price,
            "distance_from_50": round(distance_from_50, 4)
        })

    df = pd.DataFrame(contested)
    df = df.sort_values("distance_from_50", ascending=True)
    return df.head(n)

if __name__ == "__main__":
    df = most_contested_markets()
    if not df.empty:
        print(df.to_string(index=False))
