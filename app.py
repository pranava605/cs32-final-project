import streamlit as st
import pandas as pd
import plotly.graph_objects as go

from ronak_kalshiclient import trump_markets, market_prices, kalshi_request
from ronak_alerts import check_alerts_dashboard
from ronak_simulator import Bets

# CONFIGURING THE PAGE

st.set_page_config(
    # sets browser title
    page_title="Kalshi Simulator",
    # uses the entire width of the entire browser screen
    layout="wide",
)

# used AI to import CSS into the page using HTML; streamlit does not natively support a "dark" theme

# we also used AI to mess around with font sizes
st.markdown("""
<style>
body, .stApp { background-color: #0A0D11; color: #E8E9EB; }

/* make metric numbers smaller */
div[data-testid="stMetricValue"] {
    font-size: 18px !important;
}

/* labels like "Cash" */
div[data-testid="stMetricLabel"] {
    font-size: 13px !important;
}

/* delta (+/-) */
div[data-testid="stMetricDelta"] {
    font-size: 13px !important;
}
</style>
""", unsafe_allow_html=True)

# DETERMINING DIFFERENT SESSIONS STATES
# we need to initialize variables so they don't reset every time the page refreshes
# learned here: https://docs.streamlit.io/develop/api-reference/caching-and-state/st.session_state

# ensures the simulator starts with $100,000
if "bets" not in st.session_state:
    st.session_state.bets = Bets(100_000.0)

# tracks the market open in the orderbook
if "selected_ticker" not in st.session_state:
    st.session_state.selected_ticker = None

# stores the title of the selected market
if "selected_title" not in st.session_state:
    st.session_state.selected_title = None

# stores list of what user has in their portfolio
# begins with 100,000, 
# gAI added the pd.Timedelta line to create the graph immediately by putting a second point
if "portfolio_history" not in st.session_state:
    now = pd.Timestamp.now()
    st.session_state.portfolio_history = [
        {"time": now - pd.Timedelta(seconds=1), "value": 100_000.0},
        {"time": now, "value": 100_000.0},
    ]

# list of active price alerts the user has set
if "alerts" not in st.session_state:
    st.session_state.alerts = []

# tracks the currently selected market category
if "category" not in st.session_state:
    st.session_state.category = "trump"

# stores the fetched market list so we don't re-fetch every rerun
if "markets_cache" not in st.session_state:
    st.session_state.markets_cache = []

# prevents markets from re-fetching on auto-refresh of prices
if "markets_loaded" not in st.session_state:
    st.session_state.markets_loaded = False

# short cut for the function bets.buy() instead of st.session_state.bets.buy()
bets = st.session_state.bets

# HELPER FUNCTIONS

# used AI to create this function that converts a number to a dollar string
def dollar(x):
    try:
        return f"${float(x):,.2f}"
    except:
        return "—"

def get_current_price(ticker, side):
    # market_prices() in ronak_kalshiclient returns both yes and no prices as a dictionary
    # this function just pulls out the specific side we want as a single number
    # so instead of getting {"yes_ask": 0.46, "no_ask": 0.54} we just get 0.46
    prices = market_prices(ticker)
    if side == "YES":
        key = "yes_ask"
    else:
        key = "no_ask"
    try:
        return float(prices.get(key) or 0)
    except:
        # ensures it doesn't crash on a failed request
        return None

# in the app we add the orderbook as a visual, which is not a function within ronak_main
def fetch_orderbook(ticker):
    # reach /markets/{ticker}/orderbook to return bids/asks
    try:
        # gets specific market
        data = kalshi_request(f"/markets/{ticker}/orderbook", None)
        # depending on market type, there are different orderbooks
        return data.get("orderbook_fp") or data.get("orderbook") or {}
    except:
        # ensures it doesn't crash on a failed request
        return {}

# we refined our market fetching function to go to different markets as well
def fetch_markets(category):
    # if user wants trump, use existing trump_markets() function
    # otherwise, page through kalshi /events filtering by ticker prefix
    if category == "trump":
        return trump_markets()
    
    # we use a dictionary to map category names to their Kalshi ticker prefixes
    prefix = {"nba": "KXNBA", "politics": "KXPRES"}.get(category)
    # initializes an empty list of markets
    markets = []

    # kalshi uses cursor pagination, sending 100 markets at a time
    # we used AI here to help us understand and implement this

    # cursor acts as a bookmark so when kalshi sends one group we know where to add the next page
    cursor = None
    while True:
        # request 100 events at a time
        params = {"status": "open", "limit": 100, "with_nested_markets": "true"}

        # if we have a cursor from the previous page, attach it so kalshi knows where to continue
        if cursor:
            params["cursor"] = cursor
        data = kalshi_request("/events", params)

        # if request doesn't work then stop
        if not data:
            break

        # loop through each event on this page
        for event in data.get("events", []):
            et = (event.get("event_ticker") or "").upper()

            # only add events that match our category prefix (e.g. "KXNBA")
            if prefix is None or et.startswith(prefix):
                markets.extend(event.get("markets", []))

        # grab the cursor for the next page
        cursor = data.get("cursor")

        # if kalshi didn't send a cursor back, we've hit the last page
        if not cursor:
            break

    return markets

# HEADER

# this function creates a title
# learned here: https://docs.streamlit.io/develop/api-reference/text/st.markdown
st.markdown("### Kalshi Market Simulator by Pranav, Rishab, and Ronak")

# this draws a horizontal line
st.divider()

# LEFT COLUMN

# splits the page into 2 columns 
# learned here: https://docs.streamlit.io/develop/api-reference/layout/st.columns
col_left, col_right = st.columns(2)

# this is a streamlit function that refreshes the the left panel every 30s to get updated prices
# learned here: https://docs.streamlit.io/develop/api-reference/execution-flow/st.fragment
@st.fragment(run_every=15)

def left_panel():
    # Top Left Quadrant w/ Portfolio
    st.markdown("**Portfolio**")

    # this pulls from the functions that we defined in ronak_simulator.py with the Bets class
    o_pnl = bets.calc_open_pnl(get_current_price)
    r_pnl = bets.calc_realized_pnl()
    portfolio_value = bets.calc_portfolio_value(get_current_price)

    # every time the fragment reruns, record the current portfolio value with a timestamp
    # st.session_state.portfolio_history.append({
        # "time": pd.Timestamp.now(),
        # "value": portfolio_value
    #})
    # st.session_state.portfolio_history = st.session_state.portfolio_history[-100:]

    # the code above that we wrote updates every second
    # to update every 15 seconds, we consulted generative AI
    now = pd.Timestamp.now()

    if (
        not st.session_state.portfolio_history or
        (now - st.session_state.portfolio_history[-1]["time"]).total_seconds() >= 15
    ):
        st.session_state.portfolio_history.append({
            "time": now,
            "value": portfolio_value
        })

        # we only keep the last 100 data points so the list doesn't grow forever
    st.session_state.portfolio_history = st.session_state.portfolio_history[-100:]

    # we learned to use st.metric here (substituting st w/ m1 because we have multiple)
    # this shows all these quantities in the portfolio section
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Cash", dollar(bets.cash))
    m2.metric("Portfolio Value", dollar(portfolio_value))
    
    # streamlit's delta operator shows a green/red arrow if there is a gain or loss
    m3.metric("Open P&L", dollar(o_pnl), delta=f"{o_pnl:+.2f}" if o_pnl else None)
    m4.metric("Realized P&L", dollar(r_pnl), delta=f"{r_pnl:+.2f}" if r_pnl else None)

    # we want to only build a chart if we have multiple data points
    # in other words, we want to only build a chart if we have gone through multiple refreshes
    if len(st.session_state.portfolio_history) > 1:
        # get time stamps to make the x-axis and get values from history to make y-axis
        times = [h["time"] for h in st.session_state.portfolio_history]
        values = [h["value"] for h in st.session_state.portfolio_history]

        # green if portfolio is up from start of session, red if down
        line_color = "#00D26A" if values[-1] >= values[0] else "#FF4757"
        fill_color = "rgba(0,210,106,0.08)" if line_color == "#00D26A" else "rgba(255,71,87,0.08)"


        # used AI to build the plotly chart and configure axes
        # referenced https://plotly.com/python/line-charts/
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=times,
            y=values,
            mode="lines",
            line=dict(color=line_color, width=2),
            fill="tozeroy",
            fillcolor=fill_color,
        ))
        fig.update_layout(
            template="plotly_dark",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            margin=dict(l=60, r=20, t=20, b=40),
            height=200,
            showlegend=False,
            xaxis=dict(
                showgrid=True,
                gridcolor="rgba(255,255,255,0.06)",
                tickformat="%H:%M:%S",
                title="Time",
            ),
            yaxis=dict(
                showgrid=True,
                gridcolor="rgba(255,255,255,0.06)",
                tickprefix="$",
                tickformat=",.0f",
                title="Portfolio Value",
                rangemode="tozero",
            ),
        )
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
    else:
        st.caption("Portfolio chart will appear after a few refreshes.")

    st.divider()

    # Bottom Left Open Positions
    st.markdown("**Open Positions**")
    # this function displays text in small font; note %H:%M:%S is the time format
    st.caption(f"Prices last updated: {pd.Timestamp.now().strftime('%H:%M:%S')}")

    if not bets.bets:
        st.caption("No open positions. Buy a contract from the market browser.")
    else:
        # check alerts using check_alerts_dashboard() from ronak_alerts.py
        # we pass st.toast as the notification function so it displays in the dashboard
        # learned here: https://docs.streamlit.io/develop/api-reference/status/st.toast
        def notify(alert, current_cents):
            st.toast(
                f"🔔 {alert['title'][:40]} {alert['side']} is {current_cents:.0f}¢ : "
                f"{alert['condition']} {alert['threshold']:.0f}¢"
                )
        
        # will loop and check prices
        st.session_state.alerts = check_alerts_dashboard(st.session_state.alerts, notify)

        # for each position: show entry vs current, sell button, set alert button
        for i, bet in enumerate(bets.bets):
            cur = get_current_price(bet["ticker"], bet["yes_no"])
            # specific pnl calculator for the position
            pnl = (cur - float(bet["price"])) * int(bet["contracts"]) if cur else None

            # st.expander is a function that creates a box to be clicked on and expand
            # learned here: https://docs.streamlit.io/develop/api-reference/layout/st.expander

            with st.expander(f"{bet['title'][:45]} — {bet['yes_no']}"):
                c1, c2 = st.columns(2)
                c1.metric("Entry", dollar(bet["price"]))
                c2.metric("Current", dollar(cur) if cur else "—", delta=f"{pnl:+.2f}" if pnl else None)
                st.caption(f"Contracts: {bet['contracts']} | Cost: {dollar(float(bet['price']) * int(bet['contracts']))}")

                # st.button is a function that creates a button
                # learned here: https://docs.streamlit.io/develop/api-reference/widgets/st.button
                if st.button("Sell", key=f"sell_{i}"):
                    if cur:

                        # calls the resolve function from ronak_simulator.poy to close position
                        bets.resolve(bet["ticker"], cur, bet["yes_no"])
                        st.success("Position closed.")
                        st.rerun()

                st.markdown("**Set Price Alert**")

                # split into 4 columns: side, condition, threshold, set button
                # AI helped with the input parameters; particularly with the use of i so each position has a unique button id
                a1, a2, a3, a4 = st.columns(4)

                # user picks YES or NO side
                a_side = a1.selectbox("Side", ["YES", "NO"], key=f"aside_{i}")

                # user picks whether alert is for above or below a price
                a_cond = a2.selectbox("Condition", ["below", "above"], key=f"acond_{i}")

                # user types the price in cents they want to be alerted at
                # learned here: https://docs.streamlit.io/develop/api-reference/widgets/st.number_input
                a_thresh = a3.number_input("Cents", min_value=1, max_value=99, value=50, key=f"athresh_{i}")

                # add spacing so the button lines up with the other columns; used AI for this line
                a4.markdown("<br>", unsafe_allow_html=True)

                # when set is clicked, add the alert to our session state list
                if a4.button("Set", key=f"aset_{i}"):

                    # same dictionary structure as add_alert() in ronak_alerts.py
                    st.session_state.alerts.append({
                        "ticker": bet["ticker"],
                        "title": bet["title"],
                        "side": a_side,
                        "condition": a_cond,
                        "threshold": a_thresh,
                    })

                    # shows the alert user just set
                    st.success(f"Alert set: {a_side} {a_cond} {a_thresh}¢")
                    st.rerun()

with col_left:
    left_panel()

# RIGHT COLUMN

with col_right:

    # Top Right w/ Orderbook
    st.markdown("**Orderbook**")

    ticker = st.session_state.selected_ticker
    s_title = st.session_state.selected_title

    if not ticker:
        st.caption("Select a market from the browser below to see its orderbook.")
    else:
        # we ran into the problem here where we could not identify what a yes price was for (e.g. which team)
        # we used AI to add the following two lines to show who the yes price is for pulling data from Kalshi
        market_detail = next((m for m in st.session_state.markets_cache if m.get("ticker") == ticker), None)
        yes_sub = market_detail.get("yes_sub_title", "") if market_detail else ""

        
        # this part below did not work

        #if yes_sub:
            # the only way it wouldn't look weird is truncating it
            # but that would not give the full title
            # st.markdown(f'*{s_title}*')
            # st.caption(f'YES = {yes_sub}')
        # else:
            # st.markdown(f'*{s_title}*')
        # alternatively, we can wrap the text, which is what gAI helped with

        if yes_sub:
            st.markdown(f"""
            <div style="
                font-size: 18px;
                font-style: italic;
                line-height: 1.4;
                word-wrap: break-word;
            ">
                {s_title}
            </div>
            """, unsafe_allow_html=True)
            
            st.caption(f"YES = {yes_sub}")
        else:
            st.markdown(f"""
            <div style="
                font-size: 18px;
                font-style: italic;
                line-height: 1.4;
                word-wrap: break-word;
            ">
                {s_title}
            </div>
            """, unsafe_allow_html=True)        

        try:
            prices = market_prices(ticker)
            yes = float(prices.get("yes_ask") or 0)
            no = float(prices.get("no_ask") or 0)

            # side selector comes first, orderbook updates to match
            st.markdown("**Trade**")

            # the area in which you input your trade
            # same buy logic as ronak_main.py but using streamlit inputs instead of terminal input()

            t_side = st.session_state.get("trade_side", "YES")

            # input the number of contracts you want to buy with a minimum of 1
            t_contracts = st.session_state.get("trade_contracts", 1)

            if t_side == "YES":
                t_price = yes
            else:
                t_price = no

            t_cost = t_price * t_contracts

            st.caption(f'Cost per contract: {dollar(t_price)} | Total cost: {dollar(t_cost)} | Cash available: {dollar(bets.cash)}')

            # input the number of contracts you want to buy with a minimum of 1
            t1, t2 = st.columns(2)
            t_side = t1.selectbox("Side", ["YES", "NO"], key="trade_side")
            t_contracts = t2.number_input("Contracts", min_value=1, value=1, key="trade_contracts")

            ob = fetch_orderbook(ticker)

            # switch orderbook data based on selected side
            # no_dollars = NO bids = implied YES asks
            # yes_dollars = YES bids
            if t_side == "YES":
                asks = ob.get("no_dollars", [])   # NO bids are implied YES asks
                bids = ob.get("yes_dollars", [])  # YES bids directly
                last_price = yes
            else:
                asks = ob.get("yes_dollars", [])  # YES bids are implied NO asks
                bids = ob.get("no_dollars", [])   # NO bids directly
                last_price = no

            ob_rows = []

            # build asks into temp list first, then reverse so lowest ask is closest to last price
            ask_rows = []

            # used AI to help with organizing the orderbook here; it was extremely confusing to get the ordering & logic right

            # ob.get returns a list of tuples — each tuple is (price, quantity)
            # price_d is the raw dollar price (e.g. 0.97), qty is the number of contracts

            # asks: sorted high to low by raw NO bid price
            # then reversed at the end so lowest implied YES ask is closest to last price
            for price_d, qty in sorted(asks, reverse=True)[:5]:
                try:
                    p_cents = (1 - float(price_d)) * 100
                    actual_qty = float(qty)
                    # total uses the implied YES ask price, not the raw NO bid price
                    total = (1 - float(price_d)) * actual_qty
                    ask_rows.append({"Type": "Ask", "Price": f"{p_cents:.0f}¢", "Contracts": f"{actual_qty:.0f}", "Total": dollar(total)})
                except:
                    pass
            ob_rows.extend(reversed(ask_rows))

            # last price divider row
            ob_rows.append({"Type": "-", "Price": f"Last {last_price*100:.0f}¢", "Contracts": "-", "Total": "-"})

            # bids sorted descending (highest bid at top, closest to last price)
            for price_d, qty in sorted(bids, reverse=True)[:5]:
                try:
                    p_cents = float(price_d) * 100  # YES bid price directly
                    actual_qty = float(qty)
                    total = float(price_d) * actual_qty
                    ob_rows.append({"Type": "Bid", "Price": f"{p_cents:.0f}¢", "Contracts": f"{actual_qty:.0f}", "Total": dollar(total)})
                except:
                    pass

            # organize our orderbook rows into a dataframe w/ panda
            ob_df = pd.DataFrame(ob_rows)

            # style the panda: used AI to sytle it
            def style_ob(row):
                if row["Type"] == "Ask":
                    return ["color:#FF4757"] * 4
                elif row["Type"] == "Bid":
                    return ["color:#00D26A"] * 4
                return ["color:gray"] * 4

            # this function displays out panda dataframe as an interactive table
            # learned here: https://docs.streamlit.io/develop/api-reference/data/st.dataframe
            st.dataframe(
                ob_df.style.apply(style_ob, axis=1),
                hide_index=True,
                use_container_width=True,
                height=220,
            )

            
            # this is the buy button
            if st.button("Buy", key="trade_buy"):
                if t_cost > bets.cash:
                    st.error("Not enough cash.")
                else:
                    bets.buy(ticker, s_title, t_side, t_contracts, t_price)
                    st.success(f"Bought {t_contracts} x {t_side} @ {dollar(t_price)}")

                    # st.rerun refreshes the page after you have bought
                    st.rerun()

            # standalone alert with no position required
            # mirrors exactly to our alert system we did while you are in a position
            st.markdown("**Set Price Alert for this Market**")
            sa1, sa2, sa3, sa4 = st.columns(4)
            sa_side = sa1.selectbox("Side", ["YES", "NO"], key="sa_side")
            sa_cond = sa2.selectbox("Condition", ["below", "above"], key="sa_cond")
            sa_thresh = sa3.number_input("Cents", min_value=1, max_value=99, value=50, key="sa_thresh")

            # add spacing so the button lines up with the other columns; used AI for this line
            sa4.markdown("<br>", unsafe_allow_html=True)

            if sa4.button("Set Alert", key="sa_set"):
                st.session_state.alerts.append({
                    "ticker": ticker,
                    "title": s_title,
                    "side": sa_side,
                    "condition": sa_cond,
                    "threshold": sa_thresh,
                })
                st.success(f"Alert set: {sa_side} {sa_cond} {sa_thresh}¢")

        # if fetching fails then return the error message (e) and also so program doesn't crash
        except Exception as e:
            st.error(f"Could not load orderbook: {e}")

    st.divider()

    # Bottom Right w/ Market Search System
    st.markdown("**Market Browser**")

    # first we want to allow the user to choose among the three different markets that we have

    # this displays the widget to choose your option
    # learned here: https://docs.streamlit.io/develop/api-reference/widgets/st.selectbox

    category = st.selectbox(
        "Category",
        options=["trump", "nba", "politics"],

        # AI recommended that we use an internal key to transform ticker id into its corresponding title
        format_func=lambda x: {"trump": "Trump", "nba": "NBA", "politics": "Politics"}[x],

        key="category_select",
    )

    # manual refresh button appears below 
    # (we wanted it to appear side by side but ran into misalignment problems that AI could not solve)
    if st.button("Refresh", key="refresh_markets"):

        # st.spinner diplays a loading spinner while executing code
        # learned here: https://docs.streamlit.io/develop/api-reference/status/st.spinner
        with st.spinner("Loading..."):
            # fetch fresh markets and update the cache
            st.session_state.markets_cache = fetch_markets(category)
            # save the current category
            st.session_state.category = category
            # mark markets as loaded so auto-refresh doesn't re-fetch
            st.session_state.markets_loaded = True

    # only fetch markets if not loaded yet or category changed
    if not st.session_state.markets_loaded or st.session_state.category != category:
        st.session_state.category = category
        with st.spinner("Loading markets..."):
            st.session_state.markets_cache = fetch_markets(category)
            st.session_state.markets_loaded = True

    # search bar to filter the market list by title
    # learned here: https://docs.streamlit.io/develop/api-reference/widgets/st.text_input
    search = st.text_input("Search", placeholder="Filter by title...", key="market_search")

    rows = []
    for market in st.session_state.markets_cache:
        # try title first, fall back to yes_sub_title for markets that don't have a main title
        title = market.get("title") or market.get("yes_sub_title") or ""
        
        # if user typed something in search and it's not in the title, skip this market
        if search and search.lower() not in title.lower():
            continue
        
        # build a row with just the fields we want to show in the table
        rows.append({
            "Ticker": market.get("ticker", ""),
            "Title": title,
            "YES": market.get("yes_ask_dollars"),
            "NO": market.get("no_ask_dollars"),
            "Volume": market.get("volume_fp", 0),
        })

    # assembles our markets that are in rows into a data frame
    df = pd.DataFrame(rows)

    if not df.empty:
        # used AI to convert YES, NO, and Volume columns from strings to numbers so the table displays correctly
        df["YES"] = pd.to_numeric(df["YES"], errors="coerce")
        df["NO"] = pd.to_numeric(df["NO"], errors="coerce")
        df["Volume"] = pd.to_numeric(df["Volume"], errors="coerce").fillna(0)

        # this compiles everything into the streamlit data frame
        # used AI here to learn the on-select parameter to ensure the market's orderbook loads in after you click it
        event = st.dataframe(
            df,
            hide_index=True,
            height=200,
            use_container_width=True,
            on_select="rerun",
            selection_mode="single-row", # only one row can be selected at a time
            column_config={
                "YES": st.column_config.NumberColumn("YES", format="$%.2f"), # note $%.2f adds a dollar sign and this shows only 2 decimals
                "NO": st.column_config.NumberColumn("NO", format="$%.2f"),
                "Volume": st.column_config.NumberColumn("Volume", format="%.0f"),
            },
        )

        # if a row was clicked, save that market's ticker and title to session state
        # then rerun so the orderbook updates to show the selected market
        # used AI for line below
        selected = event.selection.rows if hasattr(event, "selection") else []
        if selected:
            row = df.iloc[selected[0]]
            st.session_state.selected_ticker = row["Ticker"]
            st.session_state.selected_title = row["Title"]
            st.rerun()
    else:
        st.caption("No markets found. Hit Refresh.")

# Looking at Active Alerts

# at the very bottom we want the user to be able to look at the number of alerts they have and for which game
# we also want them to be able to remove their alert

# only show the alerts section if there are active alerts
if st.session_state.alerts:
    st.divider()

    # collapsible section that shows the count of active alerts in the title
    with st.expander(f"Active Alerts ({len(st.session_state.alerts)})"):

        # loop through each alert with its index so we can remove the right one
        for i, alert in enumerate(st.session_state.alerts):

            # split each row into a wide column for the alert info and a narrow one for the button
            c1, c2 = st.columns([4, 1])

            # display the alert details in small gray text
            c1.caption(f"{alert['title'][:45]} : {alert['side']} {alert['condition']} {alert['threshold']:.0f}¢")

            # used AI for the remove button
            if c2.button("Remove", key=f"remove_alert_{i}"):
                st.session_state.alerts.pop(i)
                st.rerun()