from flask import request, jsonify
import json
from .. import main
from ... import db
from ..services import channel_service
from ...models.User import User, user_schema
from ...models.Channel import Channel, channel_schema
from sqlalchemy.sql import exists
from flask import request


@main.route("/private/", methods=["GET"])
def get_privates():
    # [GET]- Should return serverside private rooms. Path: /private/
    privates =
