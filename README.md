# cs32-final-project
My CS32 Final Project with Ronak and Rishab

This project connects to Kalshi's public API to fetch live prediction market data.

As of now, the core goal is to build a live market analysis tool that scans active
markets and computes key statistics including:

All statistics are computed from live data, organized into a clean data frame,
and displayed in a readable table that refreshes on a timer. 

Right now, it includes a few things, the main of which is a paper trading simulator. However, the core of this is an **API**, which we need to get the data from Kalshi. We needed to install **requests**, which we do by using **python3 -m pip install requests**

Throughout the project, we wrote most of the code, and the way we used generative AI was to protect our code from potential errors and to improve its efficiency.

There are four files we use:

- ronak_kalshiclient.py
- ronak_main.py
- ronak_simulator.py
- ronak_trump_display.py

**ronak_kalshiclient.py:**

This file establishes all the connections to the kalshi API server. While we wrote the vast majority of it, lines written by AI all have a comment. This includes lines 20 and 23-25, line 48, and part of line 21.

Aside from that, we learned how to use the Kalshi API from here: youtube.com/watch?reload=9&v=PQe9K2aEO5I&feature=youtu.be
_________________________________________________________

**ronak_simulator.py:**

This file establishes the Bets class, which acts as our account in our paper trading simulator. For lines 8, 40-41, 67, 72-74, 77, 83, and 140-147, we consulted AI to help see realized profit and loss later. Most of these lines were copies of existing lines, but with very minimal changes to print p&l.
_________________________________________________________

**ronak_trumpdisplay.py:**

This file helps display the markets for the user to pick. AI instructed us to import time in line 2, which helps us delay the program for visibility. This is done on line 18. _________________________________________________________

**ronak_main.py:**

Finally, last but not least, we have the file that runs it all, and brings all our functions together. We did not use AI here.

To run the program, we use **ronak_main.py**.

For a more detailed explanation of our individual lines of code (as of 4/23), we created a writeup: https://docs.google.com/document/d/1QQtO2cEXMRyxlXfbl-OIohwWmz-HlPCNTmP2Y2e6-PY/edit?tab=t.0

