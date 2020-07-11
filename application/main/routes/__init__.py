from . import user
from . import message
from . import channel
from . import challenge2
from .. import main

__all__ = ["user", "message", "channel"]

@main.route("/")
def index():
    return "<h1>Hello World!</h1>"

