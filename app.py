from flask import Flask

app = Flask(__name__)

@app.route("/")
def index():
    return "<h1>Hello World!</h1>"

@app.route("/check-username/<username>")
def check_username(username):
    print("username to check: ", username)
    return "<h1>Username {} will be checked</h1>".format(username)