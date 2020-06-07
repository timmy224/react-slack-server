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
    """
    [GET] - Returns a list of the 25 most recent server-side stored messages and returns them as a JSON response
    Path: /messages/?channelId={channel_id}
    Response Body: "messages"
    """
    sel_channel = request.args.get("channelId", None)
    print(f'Received Selected Channel: {sel_channel}')
    sel_channel_messages = message_service.get_recent_messages(int(sel_channel))

    recent_messages = json.dumps([message.__dict__ for message in sel_channel_messages])
    response = {}
    response['messages'] = recent_messages
    return response

### DATABASE ROUTES ###

@main.route("/private-messages/", methods=["GET"])
def get_private_messages():
    """
    [GET] - Grabs the private from the DB sent between two users and returns it as a JSON response
    Path: /private-messages/?user1_id={user1_id}&user2_id={user2_id}
    Response Body: "messages"

    DB Tables: "messages", "private_messages"
    """
    user1_id, user2_id = request.args.get("user1_id", None), request.args.get("user2_id", None)
    response = {}
    if user1_id is None or user2_id is None:
        response["ERROR"] = "Two user ids are required in this route"
        return jsonify(response)
    # TODO - Sleyter Database Query goes here
    messages = []
    response["messages"] = json.dumps(messages)
    return response

### EXAMPLES ###

@main.route("/message/", methods=["GET"])
def get_message():
    """
    [GET] - Grabs the message from the DB and returns it as a JSON response
    Path: /message/?message_id={message_id}
    Response Body: "message"
    
    DB tables: "messages", "private_messages", "channel_messages", "users"
    """
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
    """
    [POST] - Inserts a private message into the DB using JSON passed in as request body
    Path: /private-message
    Request Body: "sender_id", "receiver_id", "content", "sent_dt" (ex: 05/02/2020 1:23PM)
    Response Body: "successful"

    DB tables: "messages", "private_messages", "users"
    """
    data = request.json
    sender_id, content = data["sender_id"], data["content"]
    sent_dt = datetime.strptime(data["sent_dt"],  "%m/%d/%Y %I:%M%p")
    message = Message(sender_id, sent_dt, content)
    receiver = User.query.filter_by(user_id=data["receiver_id"]).one()

    message.receiver = receiver
    db.session.add(message)
    db.session.commit()

    print("SUCCESS: private_message inserted into db")
    response = {}
    response["successful"] = True
    return jsonify(response)

@main.route("/channel-message/", methods=["POST"])
def insert_channel_message():
    """
    [POST] - Inserts a channel message into the DB using JSON passed in as request body
    Path: /channel-message
    Request Body: "sender_id", "channel_id", "content", "sent_dt" (ex: 05/02/2020 1:23PM)
    Response Body: "successful"

    DB tables: "messages", "channel_messages", "channels"
    """
    data = request.json
    sender_id, content = data["sender_id"], data["content"]
    sent_dt = datetime.strptime(data["sent_dt"],  "%m/%d/%Y %I:%M%p")
    message = Message(sender_id, sent_dt, content)
    channel = Channel.query.filter_by(channel_id=data["channel_id"]).one()

    message.channel = channel
    db.session.add(message)
    db.session.commit()

    print("SUCCESS: channel_message inserted into db")
    response = {}
    response["successful"] = True
    return jsonify(response)