# cs32-final-project
My CS32 Final Project with Ronak and Rishab

This project connects to Kalshi's public API to fetch live prediction market data
and surface meaningful insights through a structured, auto-refreshing display.

The core goal is to build a real-time market analysis tool that scans active
markets and computes key statistics including:

Arbitrage opportunities: markets where yes + no price < $1, flagging any
guaranteed profit gaps

Most contested markets: markets closest to 50/50, where outcome is most uncertain

Near-certain markets: markets priced at 95%+ or 5% and below, nearly resolved

Highest volume markets: most actively traded contracts right now

Overpriced markets: where yes + no > $1, a mispricing in the opposite direction of arb

All statistics are computed from live data, organized into a clean data frame,
and displayed in a readable table that refreshes on a timer. We also plan to learn how
to styalize the outputs of our code, maybe using the rich library. Overall, the project uses the
Kalshi public API (no authentication required), pandas for data manipulation, and
Python's requests library for HTTP calls.

Given time, we hope to expand this tool to include a paper trading simulator
and a historical data explorer, allowing users to test strategies and analyze
how Kalshi markets have behaved over time as well.
