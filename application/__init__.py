from dotenv import load_dotenv
from flask import Flask
from flask_cors import CORS
from flask_socketio import SocketIO
from .models import configure_db, configure_marshmallow, configure_migrate

load_dotenv()
from .config import config

socketio = SocketIO(cors_allowed_origins="*")
db = None
ma = None

def create_app():
    global db, ma
    app = Flask(__name__)
    # Configure app
    configure_app(app)
    # Database and Migrate
    db = configure_db(app)
    ma = configure_marshmallow(app)
    migrate = configure_migrate(app, db)
    # CORS
    CORS(app)
    # Register blueprints
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)
    # Give our app socket support
    socketio.init_app(app)
    return app

def configure_app(app):
    app.config.from_object(config.getConfig())