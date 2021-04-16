import os
from flask import Flask, current_app,jsonify,request,redirect,render_template,session
import robin_stocks.robinhood as rh
import robin_stocks.gemini as gem
import robin_stocks.tda as tda
import pprint
import sys
app = Flask(__name__)
app.secret_key = "super secret key"


url = "http://localhost:5000"


@app.route('/')
def login_page():
    session['auth'] = True
    return render_template('login.html')

# Authenticate the Robinhood username and password
@app.route('/authenticate',methods=['POST','GET'])
def authenticate():
    # Login POST Request
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        print((username,password), file=sys.stderr)


        if (username or password) != '':
            message = {'message':'User authenticated'}
            
            login = rh.login(username,password)
            # Get the access token from the robinhood login
            access = login.get('access_token',None)

            if(access is not None):
                session['auth'] = True
                return redirect('/view')
            else:
                session['auth'] = False
                return redirect('/login-error')
        else:
            error = {'error':'Missing username or password'}
            session['auth'] = False
            return redirect('/login-error')

@app.route('/login-error')
def loginerror_page():
    session['auth'] = False
    return render_template('loginerror.html')


@app.route('/view')
def viewing_page():
    auth = session.get('auth',False)
    print(auth, file=sys.stderr)
    if auth is True: 
        return render_template('index.html')
    else:
        return redirect('/')



if __name__ == '__main__':
    #app.run(host='localhost',debug=True,port=4000)
    app.run(host='localhost', debug=True)
    # https://jeromeetienne.github.io/AR.js/three.js/examples/marker-training/examples/generator.html