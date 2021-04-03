import robin_stocks.robinhood as rh
import robin_stocks.gemini as gem
import robin_stocks.tda as tda
import pprint

login = rh.login("roshan.poduval@gmail.com","testpassword579")

search = input("What company do you want to know about?")
stock = rh.stocks.find_instrument_data(search)
if stock[0] is not None:
    stock = stock[0]['symbol']
    pprint.pprint(rh.stocks.get_fundamentals(stock))