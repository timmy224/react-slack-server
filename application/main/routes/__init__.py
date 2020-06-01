from . import user
from . import message
from . import channel
from .. import main

@main.route("/")
def index():
    return "<h1>Hello World!</h1>"

