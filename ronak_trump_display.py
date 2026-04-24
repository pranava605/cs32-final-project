# ai added time to pause loop for better visibility
import time

from ronak_kalshiclient import trump_markets

def display():
    while True:
        print("Please wait. Getting Live Trump Markets...")
        # can change later so it fits all
        markets = trump_markets()

        print("\n TRUMP MARKET LIST")

        if markets == []:
            print("There are no Trump markets right now.")
            
            # ai added time.sleep for same reasons as above
            time.sleep(2)

            continue
        
        count = 0

        for market in markets:
            title = market["title"]
            yes_price = market["yes_ask_dollars"]
            no_price = market["no_ask_dollars"]
            volume = market["volume_fp"]
            
            count += 1

            print(f'{count}. {title}')
            print(f'YES: {yes_price}  NO: {no_price}')
            print(f'volume: {volume} \n')
        
        print("Type the number of the market you want. \nOr press Enter to refresh the market list.")
        market_number = input("Market: ")

        if market_number == "":
            continue

        # make sure the input they gave is valid
        if market_number.isdigit():
            number = int(market_number)
            if number < 1 or number > len(markets):
                print("Invalid number")
                continue
        
        # indexing for the actual market
            selected_market = markets[number - 1]
            return selected_market
        
        else:
            print("Invalid number. Type the number of the market you want. \n Or press Enter to refresh the market list.")
            continue
            
        
        


            
