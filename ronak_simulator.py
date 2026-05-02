class Bets:
    def __init__(self, money = 100000.0):
        self.cash = money

        self.bets = []
        
        # ai added the line below, so we can see realized profit/loss later
        self.closed = []

    def buy(self, ticker, title, yes_no, contracts, price):
        price = float(price)
        contracts = int(contracts)
        cost = price * contracts
        if cost > self.cash:
            print(f'Not enough money. \nYou have ${self.cash}, but you need ${cost} \n')
            return None
        self.cash = self.cash - cost

        bet = {
            "ticker": ticker,
            "title": title,
            "yes_no": yes_no,
            "contracts": contracts,
            "price": price
        }

        # add to list of bets
        self.bets.append(bet)
        print(f'Purchased {contracts} contracts at ${price} each for {title}: {yes_no}')

        print(f'Total cost: ${cost}')
        print(f'Cash left: ${self.cash}')

    def show_bets(self, current_prices=None):
        # current_prices (optional): {ticker: {"YES": yes_ask, "NO": no_ask}} 
        print("\n Your Bets")
        print(f'Cash: ${self.cash}')

        # ai added these 2 lines to show realized p&l
        realized = sum(c["profit"] for c in self.closed)
        print(f'Realized P&L: ${realized}')

        if self.bets == []:
            print("No bets yet")
            return None

        count = 0
        total_value = 0
        total_open_pnl = 0

        # checks 

        for bet in self.bets:
            count += 1
            print(f'\n Position {count}')
            print(f'title: {bet["title"].upper()}')
            print(f'position: {bet["yes_no"]}')
            print(f'contracts: {bet["contracts"]}')
            print(f'entry price: {bet["price"]}')

            if current_prices is not None and bet["ticker"] in current_prices:
                side_prices = current_prices[bet["ticker"]]
                cp = float(side_prices[bet["yes_no"]])
                current_value = cp * bet["contracts"]
                
                # ai added for p&l
                open_pnl = current_value - bet["price"] * bet["contracts"]
                
                total_value += current_value
                
                # ai added for p&l
                total_open_pnl += open_pnl
                print(f'current price: ${cp}')
                print(f'current value: ${current_value}')
                
                # ai added for p&l
                print(f'open P&L: ${open_pnl}')

        if current_prices is not None:
            print(f'\nTotal open value: ${total_value}')
            
            # ai added for p&l
            print(f'Total open P&L: ${total_open_pnl}')

    # checks value
    # optional yes_no filter so callers can target one side when both YES and NO are held
    def value(self, ticker, current_price, yes_no=None):
        current_price = float(current_price)
        bet_exists = False
        for bet in self.bets:
            # only show bets matching the requested side (or all sides when yes_no is None)
            if bet["ticker"] == ticker and (yes_no is None or bet["yes_no"] == yes_no):
                bet_exists = True

                contracts = bet["contracts"]
                buy_price = bet["price"]

                cost = buy_price * contracts
                current_value = current_price * contracts
                profit = current_value - cost

                # prints info

                print("\n Current Value:")
                print(f'entry price: ${buy_price}')
                print(f'current price: ${current_price}')
                print(f'contracts: {contracts}')
                print(f'current value: ${current_value}')
                print(f'profit: ${profit}')

        if not bet_exists:
            print("No bet found.")


    # if they decide to sell, we do most of the same stuff as checking the price, 
    # except actually sell it and change self.cash

    def resolve(self, ticker, current_price, yes_no=None):
        # ai added optional yes_no filter so callers can target a specific side
        # when the same ticker is held on both YES and NO. Default None preserves
        # original behavior (close the first matching ticker) for the CLI.
        current_price = float(current_price)

        for bet in self.bets:
            if bet["ticker"] == ticker and (yes_no is None or bet["yes_no"] == yes_no):

                contracts = bet["contracts"]
                buy_price = bet["price"]

                cost = buy_price * contracts
                current_value = current_price * contracts
                profit = current_value - cost

                self.cash += current_value

                print("\n Bet Resolved:")
                print(f'entry price: ${buy_price}')
                print(f'sale price: ${current_price}')
                print(f'contracts: {contracts}')
                print(f'money received: ${current_value}')
                print(f'profit: ${profit}')
                print(f'current cash balance: ${self.cash}')

                # ai added for p&l appending after closing position
                self.closed.append({
                    "ticker": ticker,
                    "title": bet["title"],
                    "yes_no": bet["yes_no"],
                    "contracts": contracts,
                    "buy_price": buy_price,
                    "sell_price": current_price,
                    "profit": profit,
                })
                self.bets.remove(bet)
                break

    # helper functions that help the calculations for the app

    def calc_open_pnl(self, get_price_fn):
        # start w/ 0 profit
        total = 0.0
        # loop through each open bet
        for bet in self.bets:
            # get current price by looking at the market and side
            current_price = get_price_fn(bet["ticker"], bet["yes_no"])
            # if we get a price back
            if current_price:
                # add (current price - entry price) * total contracts to total profit
                total += (current_price - float(bet["price"])) * int(bet["contracts"])
        return total

    def calc_realized_pnl(self):
        # start with zero realized pnl
        total = 0.0
        # loop through each closed bet
        for closed_bet in self.closed:
            # add profit to realized pnl total
            total += closed_bet["profit"]
        return total

    def calc_portfolio_value(self, get_price_fn):
        # start with zero
        open_value = 0.0
        # loop through open bets
        for bet in self.bets:
            current_price = get_price_fn(bet["ticker"], bet["yes_no"])
            # if there is no price fetched use entry price to ensure it doesn't crash
            if current_price is None:
                current_price = float(bet["price"])
            # portfolio calculation
            open_value += current_price * int(bet["contracts"])
        return self.cash + open_value




  


