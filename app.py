import os
from flask import Flask, current_app
app = Flask(__name__)

# a simple page that says hello
@app.route('/hello')
def hello():
    return 'Hello, World!'

@app.route('/')
def landing_page():
    return current_app.send_static_file('index.html')


if __name__ == '__main__':
    #app.run(host='localhost',debug=True,port=4000)
    app.run(host='localhost', debug=True)
    # https://jeromeetienne.github.io/AR.js/three.js/examples/marker-training/examples/generator.html