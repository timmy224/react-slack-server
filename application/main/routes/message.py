from flask import request, jsonify
from sqlalchemy import or_
from sqlalchemy.orm import aliased
from datetime import datetime
import json
from .. import main
from ... import db
from ..services import message_service
from ...models.User import User, user_schema
from ...models.Message import Message, MessageSchema, message_schema
from ...models.Channel import Channel, channel_schema
from ...models.PrivateMessages import private_messages

@main.route("/channel-messages/", methods=["GET"])
def get_channel_messages():
    """
    [GET] - Returns a list of the 25 most recent server-side stored messages and returns them as a JSON response
    Path: /messages/?channelId={channel_id}
    Response Body: "messages"
    """
    sel_channel = request.args.get("channelId", None)
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
    Path: /private-messages/?username1={username1}&username2={username2}
    Response Body: "messages"

    DB Tables: "messages", "private_messages"
    """
    username1, username2 = request.args.get("username1", None), request.args.get("username2", None)
    # sel_private_messages =message_service.get_private_messages(username_1,username_2)
    response = {}
    if username1 is None or username2 is None:
        response["ERROR"] = "Two user ids are required in this route"
        return jsonify(response)
    # TODO - Sleyter Database Query goes here
    SendingUser = aliased(User)
    ReceivingUser = aliased(User)
    messages = Message.query.join(SendingUser).join(private_messages, Message.message_id==private_messages.c.message_id).join(ReceivingUser)\
        .filter(or_(\
        ((SendingUser.username==username1) & (ReceivingUser.username==username2)),\
        ((SendingUser.username==username2) & (ReceivingUser.username==username1))\
        )).order_by(Message.sent_dt).limit(25).all()
    response["messages"] = message_schema.dump(messages, many=True)
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
    Request Body: "sender_id", "receiver_id", "content", "sent_dt" (ex: 05/02/2020 1:23 PM)
    Response Body: "successful"

    DB tables: "messages", "private_messages", "users"
    """
    data = request.json
    sender_id, content = data["sender_id"], data["content"]
    sent_dt = datetime.strptime(data["sent_dt"],  "%m/%d/%Y %I:%M %p")
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
    Request Body: "sender_id", "channel_id", "content", "sent_dt" (ex: 05/02/2020 1:23 PM)
    Response Body: "successful"

    DB tables: "messages", "channel_messages", "channels"
    """
    data = request.json
    sender_id, content = data["sender_id"], data["content"]
    sent_dt = datetime.strptime(data["sent_dt"],  "%m/%d/%Y %I:%M %p")
    message = Message(sender_id, sent_dt, content)
    channel = Channel.query.filter_by(channel_id=data["channel_id"]).one()

    message.channel = channel
    db.session.add(message)
    db.session.commit()

    print("SUCCESS: channel_message inserted into db")
    response = {}
    response["successful"] = True
    return jsonify(response)
