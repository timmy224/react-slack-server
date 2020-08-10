from flask import request, jsonify
from flask_login import login_required
from sqlalchemy import or_
from sqlalchemy.orm import aliased
from datetime import datetime
import json
from .. import main
from ... import db
from ..services import message_service
from ...models.User import User
from ...models.Message import Message
from ...models.Channel import Channel
from ...models.PrivateMessages import private_messages
from ...models.ChannelMessages import channel_messages


@main.route("/message/channel", methods=["GET","POST"])
# @login_required
def get_channel_messages():
    
        response = {}
        sel_channel = request.args.get("channel_id", None)
        sel_channel_messages = Message.query\
                                .join(channel_messages, Message.message_id == channel_messages.c.message_id)\
                                .filter_by(channel_id = sel_channel)\
                                .order_by(Message.sent_dt)\
                                .limit(25)\
                                .all()

        chan_messages_list = message_service.pop_channel_messages_client(sel_channel_messages)
        response['messages'] = json.dumps(chan_messages_list)
        return response

@main.route("/message/channel", methods=["GET","POST"])
# @login_required
def post_channel_messages():

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


@main.route("/message/private", methods=["GET","POST"])
# @login_required
def get_private_messages():
    
        response = {}
        username1, username2 = request.args.get("username1", None), request.args.get("username2", None)
        if username1 is None or username2 is None:
            response["ERROR"] = "Two user ids are required in this route"
            return jsonify(response)

        SendingUser = aliased(User)
        ReceivingUser = aliased(User)
        messages = Message.query\
            .join(SendingUser)\
            .join(private_messages, Message.message_id==private_messages.c.message_id)\
            .join(ReceivingUser)\
            .filter(or_(\
            ((SendingUser.username==username1) & (ReceivingUser.username==username2)),\
            ((SendingUser.username==username2) & (ReceivingUser.username==username1))\
            )).order_by(Message.sent_dt)\
            .limit(25)\
            .all()

        priv_messages_list = message_service.pop_private_messages_client(messages)
        response['messages'] = json.dumps(priv_messages_list)
        return response

@main.route("/message/private", methods=["GET","POST"])
# @login_required
def post_private_messages():
    
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


