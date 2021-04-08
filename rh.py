import robin_stocks.robinhood as rh
import robin_stocks.gemini as gem
import robin_stocks.tda as tda
import pprint

login = rh.login("ruhulruzbihan@gmail.com","@Vehanwien1998")
print(login)

# if you search for 'apple' or 'alphabet' works (NOTE: Google name is not in Robinhood. Only Alphabet.)
search = input("What company do you want to know about? ")
stock = rh.stocks.find_instrument_data(search)
if stock[0] is not None:
    stock = stock[0]['symbol']
    # get stockPrice as a String
    stockPrice = ' '.join(rh.stocks.get_latest_price(stock))
    print("Current price of " + stock + ": $" + stockPrice)
    print("General information about the " + stock + " stock:")
    pprint.pprint(rh.stocks.get_fundamentals(stock))