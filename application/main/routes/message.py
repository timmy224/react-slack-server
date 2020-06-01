from flask import request, jsonify
from datetime import datetime
import json
from .. import main
from ... import db
from ..services import message_service
from ...models.User import User, user_schema
from ...models.Message import Message, message_schema
from ...models.Channel import Channel, channel_schema


@main.route("/messages/", methods=["GET"])
def get_channel_messages():
    sel_channel = request.args.get("channelId", None)
    print(f'Received Selected Channel: {sel_channel}')
    sel_channel_messages = message_service.get_recent_messages(int(sel_channel))

    recent_messages = json.dumps([message.__dict__ for message in sel_channel_messages])
    response = {}
    response['messages'] = recent_messages
    print(response)
    return response

### DATABASE ROUTES ###

@main.route("/message/", methods=["GET"])
def get_message():
    message_id = request.args.get("message_id", None)
    response = {}
    if message_id is None:
        response["ERROR"] = "Missing message_id in route"
        return jsonify(response)
    message = Message.query.filter_by(message_id=message_id).one()
    message_json = message_schema.dump(message)
    response["message"] = message_json
    return response

@main.route("/private-message/", methods=["POST"])
def insert_private_message():
    data = request.json
    sender_id, content = data["sender_id"], data["content"]
    sent_dt = datetime.strptime(data["sent_dt"],  "%m/%d/%Y %I:%M%p")
    message = Message(sender_id, sent_dt, content)
    receiver = User.query.filter_by(user_id=data["receiver_id"]).first()

    message.receiver = receiver
    db.session.add(message)
    db.session.commit()

    print("SUCCESS: private_message inserted into db")
    response = {}
    response["successful"] = True
    return jsonify(response)

@main.route("/channel-message/", methods=["POST"])
def insert_channel_message():
    data = request.json
    sender_id, content = data["sender_id"], data["content"]
    sent_dt = datetime.strptime(data["sent_dt"],  "%m/%d/%Y %I:%M%p")
    message = Message(sender_id, sent_dt, content)
    channel = Channel.query.filter_by(channel_id=data["channel_id"]).first()

    message.channel = channel
    db.session.add(message)
    db.session.commit()

    print("SUCCESS: channel_message inserted into db")
    response = {}
    response["successful"] = True
    return jsonify(response)