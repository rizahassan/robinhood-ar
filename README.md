# Robinhood AR
A web application that shows stock information in AR.

## How to run
After cloning the repository, go the RobinhoodAR directory, and run these commands on your Command Line terminal

1. On macOS: `python3 -m venv venv` to create a virtual environment.

On Windows: `py -m venv venv`

2. On macOS: `source venv/bin/activate` to activate virtual environment.

On Windows: `.\env\Scripts\activate`

3. `pip3 install -r requirements.txt` to install all dependencies

4. `python3 app.py` to run the server.

Then, search for localhost:5000 on your browser to see the web app.

### Note
Make sure to activate virtual environment before making any development. Once completed with development,
run `pip3 freeze > requirements.txt` to update the file with new dependencies