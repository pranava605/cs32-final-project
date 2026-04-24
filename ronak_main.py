from ronak_trump_display import display
from ronak_kalshiclient import market_prices
from ronak_simulator import Bets

def main():
    print("Welcome to our final project. \nBy Pranav, Rishab, Ronak \n")

    # start sim
    bets = Bets()


    while True:
        # get users market
        selected_market = display()

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
        print("\n SELECTED MARKET \n \n")
        print(f'{title.upper()}')
        print(f'YES: {yes_price}  NO: {no_price}')
        print(f'volume: {volume} \n')

        print("\n What would you like to do? \n")
        print("1. Buy YES")
        print("2. Buy NO")
        print("3. Show all my existing bets")
        print("4. Check the current value and potentially exit")
        print("5. Go back to the list of markets")
        print("6. Quit")
        
        choice = input("\n Choice Number: \n")
        
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
                        bets.value(ticker, yes_price)

                        sell = input("Do you want to sell now? (yes/no): ")
                        if sell.lower() == "yes":
                            bets.resolve(ticker, yes_price)

                    elif bet["yes_no"] == "NO":
                        bets.value(ticker, no_price)

                        sell = input("Do you want to sell now? (yes/no): ")
                        if sell.lower() == "yes":
                            bets.resolve(ticker, no_price)

                    break
        
        elif choice == "5":
            continue

        elif choice == "6":
            print("Thanks for using our project!")
            break

        else:
            print("Invalid choice.")
        
        input("\nPress Enter to Continue:")


if __name__ == "__main__":
    main()

