import os
from flask import Flask, current_app, jsonify, request, redirect, render_template, session
import robin_stocks.robinhood as rh
import robin_stocks.gemini as gem
import robin_stocks.tda as tda
import pprint
import sys
from PIL import Image
import PIL
import io
import base64
import logging
import pyotp
import requests

# Disable log in Flask server
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

app = Flask(__name__)
app.secret_key = "super secret key"
# app.config.from_object('config')
# app.config.from_pyfile('config.py')

# Host URL
url = "http://localhost:5000"

# Route to the landing page


@app.route('/')
def login_page():
    session['auth'] = True
    return render_template('login.html')

# Route to login error page


@app.route('/login-error')
def loginerror_page():
    session['auth'] = False
    return render_template('loginerror.html')

# Route to access the Augmented Reality


@app.route('/view')
def viewing_page():
    auth = session.get('auth', False)
    if auth is True:
        return render_template('index.html')
    else:
        return redirect('/')


# GET HTTP REQUEST
# URL : http://localhost:5000/stock_info

@app.route('/stock_info', methods=['GET'])
def returnStock():

    stock = rh.stocks.find_instrument_data(text_result)

    # Add stock price to dictionary
    if stock[0] is not None:
        stockPrice = (rh.stocks.get_latest_price(stock[0]["symbol"]))
        stock[0]['stockPrice'] = " ".join(stockPrice)
        return jsonify({'stocks': stock[0]})
    else: 
        return jsonify(error="Stock not found")


# GET HTTP REQUEST
# URL : http://localhost:5000/image_info
# Save the snapshot from the webcam to the camera-image directory

@app.route("/image_info", methods=['POST'])
def image_info():
    # Get the image in URI Base 64 format
    myfile = request.args.get('myimage').split(',')
    imgdata = base64.b64decode(myfile[1])
    im = Image.open(io.BytesIO(imgdata))

    # Store and display text_detect output for get request
    from cloud_detect import text_detect
    text_detect_output = text_detect(imgdata)

    # Retrieve text_detect output and send get request for stock information
    if(text_detect_output != None):
        global text_result
        text_result = text_detect_output
        stock_info = requests.get(url + '/stock_info')
        return text_detect_output
    else:
        return jsonify(error="No text detected")


# HTTP REQUEST
# URL : http://localhost:5000/authenticate
# Authenticate the Robinhood username and password
@app.route('/authenticate', methods=['POST'])
def authenticate():
    # Login POST Request
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        mfaCode = request.form['mfaCode']
        expireMin = 86400

        # If username/password/mfaCode is not empty, then complete the authentication
        if (username or password or mfaCode) != '':
            message = {'message': 'User authenticated'}
            mfaCode = mfaCode.encode("UTF-8")
            mfaCode = base64.b32encode(mfaCode)
            totp = pyotp.TOTP(mfaCode).now()

            login = rh.login(username, password, expireMin, mfa_code=totp)

            # Get the access token from the robinhood login
            access = login.get('access_token', None)

            if(access is not None):
                session['auth'] = True
                return redirect('/view')
            else:
                session['auth'] = False
                return redirect('/login-error')
        else:
            error = {'error': 'Missing username or password'}
            session['auth'] = False
            return redirect('/login-error')

# POST HTTP REQUEST
# URL : http://localhost:5000/login
# Log out user from the Robinhood account and exit the AR view


@app.route('/logout', methods=['POST'])
def logout():
    # Logout POST Request
    if request.method == 'POST':
        rh.logout()
        session['auth'] = False
        return redirect('/')


if __name__ == '__main__':
    app.run(host='localhost', debug=True)
    # https://jeromeetienne.github.io/AR.js/three.js/examples/marker-training/examples/generator.html
