# react-slack-server
Important: make sure you have Python installed locally on your machine

## Setting up: 
1. Navigate to the root project folder in command prompt: `$ cd react-slack-server`
2. Create virtual environment named env: `$ py -m venv env`
3. Activate virtual environment: `$ env\Scripts\activate`
4. Install Flask: `$ pip install flask`

## Running the server:
1. Make sure you're in the root project folder `$ cd react-slack-server`
2. Make sure your virtual environment is enabled `$ env\Scripts\activate`
3. Use debug mode `$ set FLASK_DEBUG=1`
4. Run Flask: `$ flask run`
5. Navigate to `http:/localhost:5000` in your browser

## Shutting down the server:
To kill the server enter `CTRL + C` in the command prompt

To deactivate the virtual environment when you're finished running: `$ deactivate`
