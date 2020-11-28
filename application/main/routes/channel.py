from flask import request, jsonify
from flask_login import login_required, current_user
import json
from .. import main
from ... import db
from ..services import channel_service, role_service, org_service, socket_service, event_service
from ...models.Channel import Channel, channel_schema
from ...models.ChannelMember import ChannelMember, channel_member_schema
from ...constants.roles import channel_roles
from flask_socketio import close_room
from ... import socketio

@main.route("/channel", methods=["POST", "DELETE"])
@login_required
def channels():
    if request.method == "POST":
        data = request.json
        action = data["action"]
        if action == "GET":
            org_name = data["org_name"]
            channels = channel_service.get_users_channels(current_user, org_name)
            channels_json = channel_schema.dump(channels, many=True)
            response = {}
            response["channels"] = channels_json
            return response
        elif action == "STORE":
            channel_info = data["channel_info"]
            channel_name, org_name = channel_info["name"], channel_info["orgName"]
            channel_is_available = db.session.query(
                Channel.name).filter_by(name=channel_name).scalar() is None
            if channel_is_available:
                org = org_service.get_org(org_name)
                added_usernames = channel_info["members"]
                is_private = channel_info["isPrivate"]
                if is_private:
                    usersResult = org_service.get_users_by_usernames(org, added_usernames)
                    if usersResult["usernames_not_found"]:
                        response = {
                            "ERROR": "Some users were not found",
                            "users_not_found": usersResult["usernames_not_found"]
                        }
                        return response
                    users = usersResult["users"]
                else:
                    users = org.members
                admin_username = current_user.username
                channel = channel_service.create_channel(
                    channel_name, users, is_private, admin_username, org)
                channel_id = channel_service.store_channel(channel)                                
                # get roles
                members_channel_role, admin_channel_role = role_service.get_role(
                    channel_roles.TADPOLE), role_service.get_role(channel_roles.ADMIN)
                # member ids
                admin_user_id = current_user.user_id
                member_user_ids = map(lambda user: user.user_id, users)
                # members role update
                statement = role_service.gen_channel_members_role_update_by_member_ids(
                    channel_id, member_user_ids, members_channel_role.role_id)
                db.session.execute(statement)
                # admin role update
                statement = role_service.gen_channel_members_role_update_by_member_ids(
                    channel_id, [admin_user_id], admin_channel_role.role_id)
                db.session.execute(statement)
                db.session.commit()
                # notify that permissions were updated for these users and that they've been added to a new channel
                usernames = map(lambda user: user.username, users) 
                for username in usernames:
                    socket_service.send_user(username, "permissions-updated")
                    event_service.send_added_to_channel(username, channel)
                response = {"successful": True, }
                return jsonify(response)
        else:
            response = {}
            response["ERROR"] = "Channel name is taken"
            return jsonify(response)

    elif request.method == "DELETE":
        data = request.json
        org_name, channel_name = data["org_name"], data["channel_name"]        
        channel = channel_service.get_channel(org_name, channel_name)
        channel_service.delete_channel(channel)
        event_service.send_channel_deleted(channel)
        socket_service.close_channel_room(org_name, channel_name)
        response = {}
        response['successful'] = True
        return jsonify(response)


@main.route("/channel/members", methods=["POST"])
def get_num_members():
    data = request.json
    org_name, channel_name = data["org_name"], data["channel_name"]
    channel = channel_service.get_channel(org_name, channel_name)
    num_members = len(channel.members)
    response = {'num_members': num_members}
    return response

# EXAMPLES #


@main.route("/channel-subscription/", methods=["GET", "POST"])
def channel_subscription():
    """
    IMPORTANT: for GET, only include ONE of the following parameters in the url: "user_id", "channel_id"
    [GET] - If "user_id" route parameter present, grabs the user's channels from the DB and returns it as a JSON response
    If "channel_id" route parameter present, grabs the channel's users from the DB and returns it as a JSON response
    Path: /channel-subscription/?user_id={user_id} OR 
    /channel-subscription/?channel_id={channel_id}
    Response Body: "channels" or "users"

    [POST] - Inserts a channel subscription into the DB using JSON passed in as body
    Path: /channel-subscription
    Request Body: "user_id", "channel_id"
    Response Body: "successful"
    DB tables: "users", "channels", "channel-members"
    """
    # Get user's channels (include user_id arg) OR Get channel's users (include channel_id arg)
    if request.method == "GET":
        # Only include one of the following in request url, not both
        user_id = request.args.get("user_id", None)
        channel_id = request.args.get("channel_id", None)
        response = {}
        if user_id is not None:  # Going to return this user's channels
            user = User.query.filter_by(user_id=user_id).one()
            channels_json = channel_schema.dump(user.channels, many=True)
            response["channels"] = channels_json
        elif channel_id is not None:  # Going to return this channel's users
            channel = Channel.query.filter_by(channel_id=channel_id).one()
            users_json = user_schema.dump(channel.members, many=True)
            response["users"] = users_json
        else:
            response["ERROR"] = "Missing user_id OR channel_id in route (only include one of them)"
        return response
    elif request.method == "POST":
        data = request.json
        user_id = data["user_id"]
        channel_id = data["channel_id"]
        user = User.query.filter_by(user_id=user_id).one()
        channel = Channel.query.filter_by(channel_id=channel_id).one()

        channel.members.append(user)
        db.session.commit()

        print("SUCCESS: channel_subscription inserted into db")
        response = {}
        response["successful"] = True
        return jsonify(response)


@main.route("/channel/member/", methods=["GET"])
def get_channel_members():
    """
    [GET] - grabs a channel's channel members from the DB and returns it as a JSON response (note that the ChannelMember is a join of multiple tables - see ChannelMember schema)
    Path: /channel/member/?channel_id={channel_id}
    Response Body: "channel_members"
    DB tables: "users", "channel_members", "roles"
    """
    channel_id = request.args.get("channel_id")
    response = {}
    if channel_id is None:
        response["ERROR"] = "Missing channel_id in route"
        return response
    channel_members = db.session.query(
        ChannelMember).filter_by(channel_id=channel_id).all()
    response["channel_members"] = channel_member_schema.dumps(
        channel_members, many=True)
    return response
