# react-slack-server
Important: make sure you have Python installed locally on your machine

## Setting up: 
1. Navigate to the root project folder in command prompt: `$ cd react-slack-server`
2. Create virtual environment named env: `$ py -m venv env`
3. Activate virtual environment: `$ env\Scripts\activate`
4. Install dependencies: `$ pip install -r requirements.txt`

## Create local .env file 
1. Create a file named `.env` in the project root 
2. Add `LOCAL=True` to it on the first line. All following entries should each be placed on their own line
3. Add `DATABASE_URL_PROD=` and set it to the Heroku postgres database url 
4. Add `DATABASE_URL_DEV=` and set it to your local postgres database url
5. Add `MODE=development` 

## Running the server:
1. Make sure you're in the root project folder `$ cd react-slack-server`
2. Make sure your virtual environment is enabled `$ env\Scripts\activate`
3. `$ py app.py`
4. Navigate to `http:/localhost:5000` in your browser

## Shutting down the server:
To kill the server enter `CTRL + C` twice in the command prompt quickly. If it doesn't shut down right away refresh the browser tab.

To deactivate the virtual environment when you're finished running: `$ deactivate`
