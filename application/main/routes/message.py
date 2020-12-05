from flask import request, jsonify
from flask_login import login_required, current_user
from datetime import datetime
import json
from .. import main
from ... import db
from ..services import message_service, channel_service
from ...models.User import User
from ...models.Message import Message
from ...models.Channel import Channel

@main.route("/message/channel", methods=["POST"])
# @login_required
def get_channel_messages():
        data = request.json
        org_name, channel_name = data["org_name"], data["channel_name"]
        channel = channel_service.get_channel(org_name, channel_name)        
        messages = message_service.get_channel_messages(channel)
        client_messages = message_service.populate_channel_messages_client(messages)
        response = {}
        response['messages'] = json.dumps(client_messages)
        return response


@main.route("/message/private", methods=["POST"])
# @login_required
def get_private_messages():
        data = request.json
        response = {}
        username = current_user.username
        org_name, partner_username =  data["org_name"], data["partner_username"]
        messages = message_service.get_private_messages(org_name, username, partner_username)
        client_messages = message_service.populate_private_messages_client(messages)
        response['messages'] = json.dumps(client_messages)
        return response



