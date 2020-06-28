import os
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_login import LoginManager
from flask_migrate import Migrate

def configure_db(app):
    db = SQLAlchemy(app)
    return db

def configure_marshmallow(app):
    ma = Marshmallow(app)
    return ma

def configure_migrate(app, db):
    # import tables
    from . import ChannelSubscriptions, PrivateMessages, ChannelMessages
    # import models
    from . import User, Channel, Message
    migrate = Migrate(app, db)
    return migrate
    
def configure_login(app):
    login = LoginManager(app)
    from . import User
    @login.user_loader
    def load_user(id):
        return User.query.get(int(id))
        


