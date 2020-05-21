# react-slack-server
Important: make sure you have Python installed locally on your machine

## Setting up: 
1. Navigate to the root project folder in command prompt: `$ cd react-slack-server`
2. Create virtual environment named env: `$ py -m venv env`
3. Activate virtual environment: `$ env\Scripts\activate`
4. Install dependencies: `$ pip install -r requirements.txt`
5. Create a file named `.env` in the project root and add `LOCAL=True` to it

## Running the server:
1. Make sure you're in the root project folder `$ cd react-slack-server`
2. Make sure your virtual environment is enabled `$ env\Scripts\activate`
3. `$ py app.py`
4. Navigate to `http:/localhost:5000` in your browser

## Shutting down the server:
To kill the server enter `CTRL + C` twice in the command prompt quickly. If it doesn't shut down right away refresh the browser tab.

To deactivate the virtual environment when you're finished running: `$ deactivate`
