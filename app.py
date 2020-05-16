from dotenv import load_dotenv
load_dotenv()
import os

from flask import Flask, request, jsonify
from flask_socketio import SocketIO

from routes import routes

app = Flask(__name__)
app.register_blueprint(routes)

socketio = SocketIO(app)
import socket_service

if __name__ == "__main__" and os.getenv("LOCAL") == "True":
    print("Running on http://localhost:5000/")
    socketio.run(app)

