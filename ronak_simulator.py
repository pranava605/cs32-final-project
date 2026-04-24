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
        total_value = 0.0
        total_open_pnl = 0.0

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

    def value(self, ticker, current_price):
        current_price = float(current_price)
        bet_exists = False
        for bet in self.bets:
            if bet["ticker"] == ticker:
                bet_exists = True

                contracts = bet["contracts"]
                buy_price = bet["price"]

                cost = buy_price * contracts
                current_value = current_price * contracts
                profit = current_value - cost

                print("\n Current Value:")
                print(f'entry price: ${buy_price}')
                print(f'current price: ${current_price}')
                print(f'contracts: {contracts}')
                print(f'current value: ${current_value}')
                print(f'profit: ${profit}')

        if not bet_exists:
            print("No bet found.")

    def resolve(self, ticker, current_price):
        current_price = float(current_price)

        for bet in self.bets:
            if bet["ticker"] == ticker:

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


        return None




  


