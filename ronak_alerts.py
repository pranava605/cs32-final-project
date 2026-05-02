# stores and checks different price alerts that the user may set for different markets

from ronak_kalshiclient import market_prices

# initialize a list of alerts
alerts = []

def add_alert(ticker, title, side, condition, threshold):

    # create dictionary
    alert = {
        "ticker": ticker, # specify market
        "title": title, # title of event
        "side": side, # yes or no side
        "condition": condition, # above or below price
        "threshold": threshold # what specific price
    }

    alerts.append(alert)
    # format threshold as a whole-cent integer to match the other alert messages
    print(f'\n Alert Set: Will notify if "{title}" {side} price goes {condition} {threshold:.0f}c')

def check_alerts():
    
    # check if alerts is empty
    if not alerts:
        return
    
    # initialized triggered alert list
    triggered = []

    for alert in alerts:
        # fetch prices
        prices = market_prices(alert["ticker"])

        # pull the raw price first so we can null-check before calling float()
        raw_price = prices.get("yes_ask") if alert["side"] == "YES" else prices.get("no_ask")

        # skip if Kalshi returned no price (closed market or failed request) — float(None) would crash
        if raw_price is None:
            continue

        # safe now that None is filtered out — convert dollars to cents
        current = float(raw_price) * 100

        # now mapping the alert logic; kinda self explanatory as it is a bunch of conditions
        # f strings print the alert message following a successful detection

        if alert["condition"] == "below" and current < alert["threshold"]:
            print(f"\n *** ALERT TRIGGERED ***")
            print(f" {alert['title']}")
            print(f" {alert['side']} is now {current:.0f}c — went below {alert['threshold']:.0f}c")
            # add to triggered list
            triggered.append(alert)

        elif alert["condition"] == "above" and current > alert["threshold"]:
            print(f"\n *** ALERT TRIGGERED ***")
            print(f" {alert['title']}")
            print(f" {alert['side']} is now {current:.0f}c — went above {alert['threshold']:.0f}c")
            # add to triggered list
            triggered.append(alert)

    # if an alert is triggered we need to remove it from our list of alerts
    for alert in triggered:
        alerts.remove(alert)

def show_alerts():
    # if not alerts, tell user that
    if not alerts:
        print("\n No active alerts.")
        return
    
    print("\n Active Alerts:")
    # used AI to learn the enumerate function to display all the different alerts that are active
    for i, alert in enumerate(alerts):
        print(f" {i+1}. {alert['title']} — {alert['side']} {alert['condition']} {alert['threshold']:.0f}c")

# now the code that we've previously written has helped our print version of our code
# we need to convert it to something that our dashboard can use
# using similar logic we pass a notifcation with this function below

def check_alerts_dashboard(alerts, notification):
    remaining = []
    triggered = []

    for alert in alerts:
        prices = market_prices(alert["ticker"])

        # same null-check pattern as the CLI version above
        raw_price = prices.get("yes_ask") if alert["side"] == "YES" else prices.get("no_ask")

        # keep the alert alive for the next poll instead of dropping it on a transient API failure
        if raw_price is None:
            remaining.append(alert)
            continue

        current = float(raw_price) * 100

        if alert["condition"] == "below" and current < alert["threshold"]:
            notification(alert, current)
            triggered.append(alert)

        elif alert["condition"] == "above" and current > alert["threshold"]:
            notification(alert, current)
            triggered.append(alert)

        else:
            remaining.append(alert)

    return remaining
