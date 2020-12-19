from flask import request, jsonify
from flask_login import login_required, current_user
import json
from .. import main
from ... import db
from ..services import channel_service, role_service, org_service, socket_service, event_service, user_service, client_service
from ...models.Channel import Channel, channel_schema
from ...models.ChannelMember import ChannelMember, channel_member_schema
from ...constants.roles import channel_roles
from flask_socketio import close_room, leave_room
from ... import socketio


@main.route("/channel", methods=["POST", "DELETE"])
@login_required
def channels():
    if request.method == "POST":
        data = request.json
        action = data["action"]
        if action == "GET":
            org_name = data["org_name"]
            channels = channel_service.get_users_channels(
                current_user, org_name)
            channels_json = channel_schema.dump(channels, many=True)
            response = {}
            response["channels"] = channels_json
            return response
        elif action == "STORE":
            channel_info = data["channel_info"]
            channel_name, org_name = channel_info["name"], channel_info["orgName"]
            org = org_service.get_org(org_name)
            channel_is_available = channel_service.is_channel_name_available(
                org, channel_name)
            if channel_is_available:
                added_usernames = channel_info["members"]
                is_private = channel_info["isPrivate"]
                if is_private:
                    usersResult = org_service.get_users_by_usernames(
                        org, added_usernames)
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
                    event_service.send_permissions_updated(username)
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


@main.route("/channel/members/", methods=["GET", "POST", "DELETE"])
def channel_members_info():
    """  
    Request method : POST:  
    [action: GET] - retrives all users that are a part of the channel currently
    Request Body: "action", "channel_name"
    DB tables : " channel_members"
    [action: STORE] - stores an user into the channel.members and the adds a channel role of tadpole (by default) to this user 
    Request Body: "action", "new_member_username", "channel_name" 
    DB tables: "channel_members"

    Request method : "DELETE":
    - Removes user from channel_members of the current channel
    Request Body: "removed_username", "channel_name"
    DB tables" channel_members"
    """
    response = {}
    data = request.json
    print(data)
    channel_name = data["channel_name"]
    org_name = data["org_name"]
    channel = channel_service.get_channel(org_name, channel_name)
    channel_id = channel.channel_id
    username = current_user.username
    if request.method == "POST":
        action = data["action"]
        if action == "GET":
            channel_members = db.session.query(
                ChannelMember.username).filter_by(channel_id=channel_id).all()
            channel_members_json = channel_member_schema.dumps(
                channel_members, many=True)
            response["channel_members"] = channel_members_json
            return response
        elif action == "STORE":
            new_member_username = data["new_member_username"]
            new_member = user_service.get_user(new_member_username)
            channel_service.add_channel_member(channel, new_member)
            # Updating role to tadPole after added to channel
            channel_service.set_channel_member_role(channel_id, new_member)
            data_send = {"channel_name": channel_name,
                         "added_username": new_member_username,
                         "org_name": org_name}
            # socketio.emit("channel-member-added", data_send, room=channel_id)
            socket_service.send_user(new_member_username, "permissions-updated")
            socket_service.send_user(new_member_username,
                                "added-to-channel", data_send)
            response['successful'] = True
            return jsonify(response)

    elif request.method == "DELETE":
        removed_username = data["removed_username"]
        print("removed_username: ", removed_username)
        channel_service.delete_channel_user(channel, removed_username)
        data_send = {"channel_name": channel_name,
                     "removed_username": removed_username, "channel_id": channel_id, "org_name": org_name}
        socket_service.send_channel(
            org_name, channel_name, "channel-member-removed", data_send)
        # socketio.emit("channel-member-removed", data_send, room=channel_id)
        response['successful'] = True
        return jsonify(response)

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
