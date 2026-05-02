from ronak_trump_display import display
from ronak_kalshiclient import market_prices
from ronak_simulator import Bets
from ronak_alerts import add_alert, check_alerts, show_alerts
import time

def main():
    print("Welcome to our final project. \nBy Pranav, Rishab, Ronak \n")

    # start sim
    bets = Bets()


    while True:
        # alerts are always checked
        check_alerts()
        
        # get users market
        selected_market = display()

        # basic info and stuff
        title = selected_market["title"]
        ticker = selected_market["ticker"]
        volume = selected_market["volume_fp"]

        # updated prices for specific market
        prices = market_prices(ticker)
        yes_price = prices["yes_ask"]
        no_price = prices["no_ask"]

        # print the selected market information
        print("\nSELECTED MARKET: \n")
        print(f'{title.upper()}')
        # float to handle decimals & we limit to three decimal places
        print(f'YES: {float(yes_price):.3f}  NO: {float(no_price):.3f}')
        print(f'volume: {volume} \n')
        
        # this inner loop stays on a specific market untilt he user wishes to go back to market list
        while True:

            # add a delay so the user gets to see their output before being swarmed by all the options again
            time.sleep(4)

            # prints options
            print("\nWhat would you like to do? \n")
            print("1. Buy YES")
            print("2. Buy NO")
            print("3. Show all my existing bets")
            print("4. Check the current value and potentially exit")
            print("5. Set a price alert for this market")
            print("6. View active alerts")
            print("7. Go back to the list of markets")
            print("8. Quit")
            
            
            choice = input("\nChoice Number: ")
            
            # gives options, runs functions to buy yes/no, show, etc
            if choice == "1":
                contracts = int(input(f'How many YES contracts of \"{title}\" do you want to buy? '))
                bets.buy(ticker, title, "YES", contracts, yes_price)

            elif choice == "2":
                contracts = int(input(f'How many NO contracts of \"{title}\" do you want to buy? '))
                bets.buy(ticker, title, "NO", contracts, no_price)

            elif choice == "3":
                bets.show_bets()

            elif choice == "4":
                for bet in bets.bets:
                    if bet["ticker"] == ticker:
                        if bet["yes_no"] == "YES":
                            # pass "YES" so we don't price the NO position at the YES ask
                            bets.value(ticker, yes_price, "YES")

                            sell = input("Do you want to sell now? (yes/no): ")
                            if sell.lower() == "yes":
                                # pass "YES" so resolve closes the YES position, not whichever side appears first
                                bets.resolve(ticker, yes_price, "YES")

                        elif bet["yes_no"] == "NO":
                            # pass "NO" so we don't price the YES position at the NO ask
                            bets.value(ticker, no_price, "NO")

                            sell = input("Do you want to sell now? (yes/no): ")
                            if sell.lower() == "yes":
                                # pass "NO" so resolve closes the NO position, not whichever side appears first
                                bets.resolve(ticker, no_price, "NO")

                        break
            
            elif choice == "5":
                side = input("Which side? (YES/NO): ").upper()
                condition = input("Alert when price goes (above/below): ").lower()
                threshold = float(input("At what price in cents? "))
                add_alert(ticker, title, side, condition, threshold)

            elif choice == "6":
                show_alerts()

            elif choice == "7":
                # break inner loop and goes back to the market list
                break

            elif choice == "8":
                print("Thanks for using our project!")
                return

            else:
                print("Invalid choice.")
        

if __name__ == "__main__":
    main()

