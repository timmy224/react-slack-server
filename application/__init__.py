import os
from dotenv import load_dotenv
from flask import Flask
from flask_cors import CORS
from flask_wtf.csrf import CSRFProtect
from flask_socketio import SocketIO
from .models import configure_db, configure_marshmallow, configure_migrate, configure_login

# Python standard libraries
import json

# Third-party libraries
from flask import redirect, request, url_for
from flask_login import (
    LoginManager,
    current_user,
    login_required,
    login_user,
    logout_user,
)
from oauthlib.oauth2 import WebApplicationClient


load_dotenv()
from .config import config

socketio = SocketIO(cors_allowed_origins="*")
db = None
ma = None

# OAuth 2 client setup
client = WebApplicationClient(os.getenv("GOOGLE_CLIENT_ID"))

def create_app():
    global db, ma
    app = Flask(__name__)
    app.secret_key = os.getenv("SECRET")
    # Configure app
    configure_app(app)
    # Database and Migrate
    db = configure_db(app)
    ma = configure_marshmallow(app)
    migrate = configure_migrate(app, db)
    # Configure Flask-Login
    configure_login(app)
    # CSRF
    csrf = CSRFProtect(app)
    # CORS
    CORS(app, origins=["http://localhost:3000", "https://react-slack-client.herokuapp.com"], supports_credentials=True, expose_headers=["csrf-token"])

    # Register blueprints
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)
    # Give our app socket support
    socketio.init_app(app)
    return app

def configure_app(app):
    app.config.from_object(config.getConfig())