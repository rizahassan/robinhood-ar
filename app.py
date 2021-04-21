import os
from flask import Flask, current_app,jsonify,request,redirect,render_template,session
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


# Disable log in Flask server
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

app = Flask(__name__, instance_relative_config=True)
app.config.from_object('config')
app.config.from_pyfile('config.py')

# Host URL
url = "http://localhost:5000"

# Route to the landing page
@app.route('/')
def login_page():
    session['auth'] = True
    return render_template('login.html')

# GET HTTP REQUEST
# URL : http://localhost:5000/image_info
# Save the snapshot from the webcam to the camera-image directory
@app.route("/image_info",methods= ['GET'])
def image_info():
    # Get the image in URI Base 64 format
    myfile= request.args.get('myimage').split(',')
    imgdata = base64.b64decode(myfile[1])
    im = Image.open(io.BytesIO(imgdata))

    # Save the latest snapshot to the camera-image directory in a .png format
    __location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))
    fileName="image.png"
    imagePath =os.path.join(__location__, 'camera-image/image.png')
    im.save(imagePath,'png')

    width, height = im.size
    imgformat=im.format
    return jsonify(width=width,height=height,imgformat=imgformat)


# HTTP REQUEST
# URL : http://localhost:5000/authenticate
# Authenticate the Robinhood username and password
@app.route('/authenticate',methods=['POST'])
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
            session['auth'] = Falsegit 
            return redirect('/login-error')

# Route to login error page
@app.route('/login-error')
def loginerror_page():
    session['auth'] = False
    return render_template('loginerror.html')

# Route to access the Augmented Reality
@app.route('/view')
def viewing_page():
    auth = session.get('auth',False)
    if auth is True: 
        return render_template('index.html')
    else:
        return redirect('/')



if __name__ == '__main__':
    app.run(host='localhost', debug=True)
    # https://jeromeetienne.github.io/AR.js/three.js/examples/marker-training/examples/generator.html