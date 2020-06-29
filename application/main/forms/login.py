"""
    At the moment this isn't used for anything but we'll probably use this kind of setup for server-side form validation. Leaving here for now so that we can reference it and use it in a future experiment
"""

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField

class LoginForm(FlaskForm):
    username = StringField("username")
    password = PasswordField("username")