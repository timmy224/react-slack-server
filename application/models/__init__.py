import os
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate

def configure_db(app):
    # global db
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
    db = SQLAlchemy(app)
    return db

def configure_marshmallow(app):
    ma = Marshmallow(app)
    return ma

def configure_migrate(app, db):
    # import tables
    from . import ChannelSubscriptions, PrivateMessages, ChannelMessages
    # import models
    from . import User, Message, Channel
    migrate = Migrate(app, db)
    return migrate
    

