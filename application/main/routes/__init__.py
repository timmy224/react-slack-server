from . import user
from . import message
from . import channel
from . import cookie
from . import auth
from .. import main

__all__ = ["user", "message", "channel", "cookie", "auth"]

@main.route("/")
def index():
    return "<h1>Hello World!</h1>"

