from dotenv import load_dotenv
from flask import Flask
from flask_cors import CORS
from flask_socketio import SocketIO

load_dotenv()
import os

socketio = SocketIO(cors_allowed_origins="*")
db = None

def create_app():
    global db
    app = Flask(__name__)
    # Database and Migrate
    from .models import configure_db, configure_migrate
    db = configure_db(app)
    migrate = configure_migrate(app, db)
    # CORS
    CORS(app)
    # Register blueprints
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)
    # Give our app socket support
    socketio.init_app(app)
    return app

