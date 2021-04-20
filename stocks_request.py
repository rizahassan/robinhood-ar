from flask import Flask
from flask import jsonify
from flask import request
import robin_stocks.robinhood as rh
import robin_stocks.gemini as gem
import robin_stocks.tda as tda
import pprint


app = Flask(__name__)

# From code example
quarks = [{'name': 'up', 'charge': '+2/3'},
          {'name': 'down', 'charge': '-1/3'},
          {'name': 'charm', 'charge': '+2/3'},
          {'name': 'strange', 'charge': '-1/3'}]


stocks = []


@app.route('/', methods=['GET'])
def hello_world():
    return jsonify({'message': 'Hello, World!'})


# Get stock information
@app.route('/quarks', methods=['GET'])
def returnAll():
    login = rh.login("roshan.poduval@gmail.com", "testpassword579")

# if you search for 'apple' or 'alphabet' works (NOTE: Google name is not in Robinhood. Only Alphabet.)
    search = input("What company do you want to know about? ")
    stock = rh.stocks.find_instrument_data(search)

    # Add stock price to dictionary
    if stock[0] is not None:
        stockPrice = (rh.stocks.get_latest_price(stock[0]["symbol"]))
        stock[0]['stockPrice'] = " ".join(stockPrice)

        # delete any stock information if needed
        # del stock[0]['url']

    return jsonify({'stocks': stock})
    # return jsonify({'quarks': quarks})


@app.route('/quarks/<string:name>', methods=['GET'])
def returnOne(name):
    theOne = quarks[0]
    for i, q in enumerate(quarks):
        if q['name'] == name:
            theOne = quarks[i]
    return jsonify({'quarks': theOne})


@app.route('/quarks', methods=['POST'])
def addOne():
    new_quark = request.get_json()
    quarks.append(new_quark)
    return jsonify({'quarks': quarks})


@app.route('/quarks/<string:name>', methods=['PUT'])
def editOne(name):
    new_quark = request.get_json()
    for i, q in enumerate(quarks):
        if q['name'] == name:
            quarks[i] = new_quark
    qs = request.get_json()
    return jsonify({'quarks': quarks})


@app.route('/quarks/<string:name>', methods=['DELETE'])
def deleteOne(name):
    for i, q in enumerate(quarks):
        if q['name'] == name:
            del quarks[i]
    return jsonify({'quarks': quarks})


if __name__ == "__main__":
    app.run(debug=True)
