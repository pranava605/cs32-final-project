# cs32-final-project
CS32 Final Project with Pranav, Ronak, and Rishab

This project connects to Kalshi's public API to fetch live prediction market data.

As of now, the core goal is to build a live market analysis tool that scans active
markets and computes key statistics including:

All statistics are computed from live data, organized into a clean data frame,
and displayed in a readable table that refreshes on a timer. 

Right now, it includes a few things, the main of which is a paper trading simulator. However, the core of this is an **API**, which we need to get the data from Kalshi. We needed to install **requests**, which we do by using **python3 -m pip install requests**

Throughout the project, we wrote most of the code, and the way we used generative AI was to protect our code from potential errors and to improve its efficiency.

There are seven files included:

- ronak_kalshiclient.py
- ronak_simulator.py
- ronak_trump_display.py
- ronak_alerts.py
- ronak_main.py
- requirements.txt
- app.py
_________________________________________________________

**ronak_kalshiclient.py:**

This file establishes all the connections to the kalshi API server. While we wrote the vast majority of it, lines written by AI all have a comment. This includes lines 20 and 23-25, line 48, and part of line 21.

Aside from that, we learned how to use the Kalshi API from here: youtube.com/watch?reload=9&v=PQe9K2aEO5I&feature=youtu.be and https://docs.kalshi.com/getting_started/quick_start_market_data

_________________________________________________________

**ronak_simulator.py:**

This file establishes the Bets class, which acts as our account in our paper trading simulator. For lines 8, 40-41, 67, 72-74, 77, 83, and 140-147, we consulted AI to help see realized profit and loss later. Most of these lines were copies of existing lines, but with very minimal changes to print p&l. We later added three new methods: calc_open_pnl, calc_realized_pnl, and calc_portfolio_value. We did this so that app.py could pull these calculations directly from the Bets class instead of duplicating the logic in the dashboard file.

_________________________________________________________

**ronak_trumpdisplay.py:**

This file helps display the markets for the user to pick. AI instructed us to import time in line 2, which helps us delay the program for visibility. This is done on line 18.

_________________________________________________________

**ronak_alerts.py**

This file handles all price alert logic. It lets users set alerts for specific markets and sides, checks whether any prices have crossed their thresholds, and notifies the user when they do.

It includes both the functions that are used in the terminal version of our code as well as their mofied version that are used in the dashboard.

Nearly all of the code here was written by us, however generative AI helped with lines 73-74, with the enumerate function, so we could display all the different alerts that are active. Furthermore, AI taught us about using :.0f for rounding, which is used in lines 50, 57, and 74. 

_________________________________________________________

**ronak_main.py:**

This is the file that runs it all, and brings all our functions together. We did not use AI here.

To run the program, we use **python ronak_main.py**.

This prints all of the important outputs only using the terminal and allows the user to interact with our paper trading simulator without a dashboard, natively with python.

For a more detailed explanation of our individual lines of code (as of 4/23), we created a writeup: https://docs.google.com/document/d/1QQtO2cEXMRyxlXfbl-OIohwWmz-HlPCNTmP2Y2e6-PY/edit?tab=t.0

_________________________________________________________

**requirements.txt**

This is a file that contains the different versions of each package needed to run our code.

_________________________________________________________

**app.py**

This file is our Streamlit dashboard. This is a single page visual interface built on top of the existing CLI project. It pulls from ronak_kalshiclient.py to get live market data, and ronak_simulator.py and ronak_alerts.py to manage positions and alerts. We wrote the majority of it, but used AI to help with the orderbook logic, plotly chart, and several Streamlit-specific functions we had not seen before. 

To run the dashboard, use *streamlit run app.py*

Then open *http://localhost:8501*.

If streamlit is not installed, run *pip install -r requirements.txt* or *pip3 install -r requirements.txt*

We referenced a lot of tutorials on the functions to write our code. There are quite a lot and they are linked below. These forums were extremely helpful.

Streamlit:

https://docs.streamlit.io/get-started/fundamentals/main-concepts

https://docs.streamlit.io/develop/api-reference/caching-and-state/st.session_state

https://docs.streamlit.io/develop/api-reference/text/st.markdown

https://docs.streamlit.io/develop/api-reference/layout/st.columns

https://docs.streamlit.io/develop/api-reference/execution-flow/st.fragment

https://docs.streamlit.io/develop/api-reference/status/st.toast

https://docs.streamlit.io/develop/api-reference/text/st.caption

https://docs.streamlit.io/develop/api-reference/layout/st.expander

https://docs.streamlit.io/develop/api-reference/widgets/st.button

https://docs.streamlit.io/develop/api-reference/widgets/st.number_input

https://docs.streamlit.io/develop/api-reference/data/st.dataframe

https://docs.streamlit.io/develop/api-reference/widgets/st.selectbox

https://docs.streamlit.io/develop/api-reference/status/st.spinner

https://docs.streamlit.io/develop/api-reference/widgets/st.text_input

Plotly:

https://plotly.com/python/line-charts/

Beyond these links, we used generative AI to improve the functionality of our code, most often with the physical formatting of the dashboard. Our uses of generative AI for app.py are listed below:

For lines 22-40, AI helped us edit the font size. Without this, our code would cut off the numbers like portfolio value, cash, etc. Now, the font is smaller, so it all fits. We tested different sizes and determined that the current sizes we choise made the dashboard look best.

AI helped with line 64 and used pd.Timedelta. This enables the graph of the portfolio value to appear right away (1 second after, to be more precise) when the program begins.

We also used AI for lines 90 to 94, which convert numbers to dollar strings.

Inside our fetch_markets function, on line 124, we used AI to help us understand cursor pagination, so we could go through all the markets and access them.

Next, we consulted generative AI for lines 207-216, to ensure the portfolio value reloads every 15 seconds. Without AI, it was refreshing constantly, so the user might have been overwhelmed by the constantly changing numbers. We might consider altering this 15 second value in the future, but for now this is another example of how we used generative AI to improve the user experience.

Generative AI also helped us improve lines 228 and 229 by using :+.2f.

For the chart itself (starting line 244), we used https://plotly.com/python/line-charts/ as we mentioned above, and also got help from generative AI to create/configure the axes, margins, and tickmarks.

For lines 380-381, we used AI to add two lines to show who the yes price is for pulling data from Kalshi.

In addition, once our code from lines 386-393 did not correctly format and display the prices, we asked AI how we could wrap the text, which is shown below that. This ensures the event names are fully printed when placing an order, so you know the entirety of what you're betting on.

For the actual organizing of the orderbook, it was extremely confusing to get the ordering & logic right. AI helped us sort it, starting in line 476, by high to low by the raw NO bid price, and then it's reversed at the end so the lowest implied YES ask will be closest to the last price. Then, to best create the panda, at line 500, including organizing our orderbook rows into a dataframe, and styling it, we used AI.

Then, we noticed there was an issue with spacing, so in order to add spacing so the buttons lined up with the other columns, generative AI helped us with lines 541-551.

For line 572, AI recommended that we use an internal key to transform the ticker id into its corresponding title.

Then, for lines 624-627, we kept getting errors, so generative AI assisted us with converting the YES, NO, and Volumecolumns from strings to numbers so the table displays correctly without errors.

In and around line 630, we used AI to learn the on-select parameter to ensure the market's orderbook loads in after you click it.

We also wanted to ensure that if a row was clicked, our program would save that market's ticker and title to session state (essentially it would mean the market is selected). Then, it would rerun so the orderbook updates to show the selected market. AI helped us add line 648 to complete this task.

Finally, we were struggling to create a button to remove alerts, so AI assisted us with the remove button, from line 679 to 681.

_________________________________________________________

Nearly 2000 lines of code and 50+ hours spent later, we truly feel like we learned a lot throughout this project. Our hope is that this program, considering its actual and real time functionality, can eventually be used alongside actual Kalshi trading with the new tools we added that Kalshi doesn't currently show.

Thank you for reading and using our program.

- Pranav, Rishab, Ronak
