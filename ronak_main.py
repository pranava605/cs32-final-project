from ronak_trump_display import display
from ronak_kalshiclient import market_prices
from ronak_simulator import Bets

import time

def main():
    print("Welcome to our final project.\nBy Pranav, Rishab, Ronak \n")

    # start sim
    bets = Bets()


    while True:
        # prints options
        print("\nWhat would you like to do?\n")
        print("1. See Markets")
        print("2. View Existing Bets")
        print("3. Check Live Portfolio")
        print("4. Quit")
        
        decision = input("\nChoice Number:\n")
        
        if decision == "1":
        # get users market
            selected_market = display()

            # added by ai -> if the user quits when looking at markets, then the program doesn't break
            if selected_market is None:
                continue

            # basic info and stuff
            title = selected_market["title"]
            ticker = selected_market["ticker"]
            volume = selected_market["volume_fp"]

            # updated prices for  specific market
            # PRANAV AND RISHAB ---- THIS IS WHERE WE ARE GOING TO ADD MORE COMPLEXITY (USING MARKET_PRICES)
            prices = market_prices(ticker)
            yes_price = prices["yes_ask"]
            no_price = prices["no_ask"]

            # print the selected market information
            print("\nSELECTED MARKET\n\n")
            print(f'{title.upper()}')
            print(f'YES: {yes_price}  NO: {no_price}')
            print(f'volume: {volume} \n')

        # prints options
            print("\nWhat would you like to do?\n")
            print("1. Buy YES")
            print("2. Buy NO")
            print("3. Return to Main Menu")
        
        
            choice = input("\nChoice Number:\n")
        
        # gives options, runs functions to buy yes/no, show, etc
            if choice == "1":
                contracts = int(input(f'How many YES contracts of \"{title}\" do you want to buy? '))
                bets.buy(ticker, title, "YES", contracts, yes_price)

            elif choice == "2":
                contracts = int(input(f'How many NO contracts of \"{title}\" do you want to buy? '))
                bets.buy(ticker, title, "NO", contracts, no_price)

            else:
                print("Returning to Main Menu")
        
        elif decision == "2":
                bets.show_bets()
        
        elif decision == "3":
            if bets.bets == []:
                print("No bets in portfolio.")
                continue

            print("\nPORTFOLIO\n")

            count = 1

            for bet in bets.bets:
                ticker = bet["ticker"]
                prices = market_prices(ticker)

                if bet["yes_no"] == "YES":
                    current_price = prices["yes_ask"]
                else:
                    current_price = prices["no_ask"]

                print(f'\nPosition {count}: {bet["title"]} -- {bet["yes_no"]}')
                bets.value(ticker, current_price)

                count += 1

            close = input("\nIf you would like to sell, enter the position number. Otherwise, press Enter to go back")

            if close == "":
                continue

            if close.isdigit():
                close = int(close)

                if close > 0 and close <= len(bets.bets):
                    bet = bets.bets[close - 1]
                    ticker = bet["ticker"]

                    prices = market_prices(ticker)

                    if bet["yes_no"] == "YES":
                        current_price = prices["yes_ask"]
                    else:
                        current_price = prices["no_ask"]

                    sell = input("Are you sure you want to sell this position? (yes/no): ")
                    if sell.lower() == "yes":
                        bets.resolve(ticker, current_price)
                else:
                    print("Invalid position number.")
            else:
                print("Invalid input.")
            
        elif decision == "4":
                print("Thanks for using our project!")
                break


if __name__ == "__main__":
    main()

