# Import modules, you may need to install bs4
import requests, os
from bs4 import BeautifulSoup
import datetime, json

# Get the page to scrape
r = requests.get("https://blockchair.com/")
# Parse the page with BeautifulSoup as html
html = BeautifulSoup(r.content, 'html.parser')

# TEST: Write the html to a file
#with open("blockchair.html","w", encoding="UTF-8") as f:
#   f.write(html.prettify())
    
# Get all the coins, this is a list of <a> tags
all_coins = html.find_all('a', class_='explore-card-wrap')
# Get coins from the smaller cards
all_coins.extend(html.find_all('a', class_='explore-card-sm-wrap'))

# Clear the screen
def clear_screen():
    # Check if the OS is windows or not, then clear the screen
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')
        
# Get all the coins
def get_all_coins():
    # Create an empty list
    currencies = []
    for i in all_coins:
        i: BeautifulSoup
        # Get the name of the coin and add it to the list
        name = i.find('h5', class_='h5 explore-card__header__text__name')
        if name is None:
            name = i.find('h5', class_='h5 explore-card-sm__name')
        currencies.append(name.text.strip().split('\n')[0])
    return currencies

# Get the current price of a coin
def get_current_price(coin:str):
    # Replace spaces with dashes if there are any
    coin = coin.replace(' ','-')
    result = None
    for i in all_coins:
        i: BeautifulSoup
        # Get the name of the coin and add it to the list
        if "/"+coin.lower() == i['href'].lower():
            f = i.find('span', class_='price-usd')
            result = f.text.strip()
            break
    # Dictionary to return
    dictionary = {
        'name': coin.replace('-',' '),
        'price_string': result,
        'price': float(result.replace('$','').replace(',','')),
        'denomination': 'USD'
    }
    return dictionary

# Select a coin
def select_coin():
    # Coin selection menu
    coins = get_all_coins()
    print("Select a coin:")
    for i in range(len(coins)):
        print(f"{i+1}. {coins[i]}")
    choice = int(input("Enter a number: "))
    return coins[choice-1]

# Get all the prices
def get_all_prices():
    result = ""
    # First get all the coins, with prices
    coins = get_all_coins()
    # Then display the prices
    for i in coins:
        price = get_current_price(i)
        result += f"{price['name']} is currently {price['price_string']}\n"
    return result

# Get a dictionary of all the prices
def get_price_dictionary():
    # First get all the coins, with prices
    coins = get_all_coins()
    result = {}
    for i in coins:
        # Get the current price of the coin
        current_coint = get_current_price(i)
        # Add the coin to the dictionary
        result[current_coint['name']] = {
            "price_string": current_coint['price_string'],
            "price": current_coint['price'],
            "denomination": current_coint['denomination']
        }
    return result

# Saves the prices to a json file in the desired location
def save_prices(location = "prices.json"):
    time = datetime.datetime.now()
    # Add timestamp to the dictionary
    price_dict = {"__time__": str(time)}
    price_dict['__unix__'] = time.timestamp()
    price_dict.update(get_price_dictionary())
    
    # Save the dictionary to a json file
    with open(location,"w") as f:
        json.dump(price_dict, f, indent=4)
    
if __name__ == "__main__":
    # Called when the file is run directly
    clear_screen()
    print(get_all_prices())
    timestamp = int(datetime.datetime.now().timestamp())
    if not os.path.exists("prices"): 
        os.mkdir("prices")
    save_prices(location="prices/"+str(timestamp)+".json")

        