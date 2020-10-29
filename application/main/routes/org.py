from flask import request, jsonify
import json
from flask_login import login_required, current_user
from .. import main
from ... import db
from ..services import org_service, user_service, client_service, role_service, socket_service, permission_service
from ...models.OrgMember import OrgMember, org_member_schema
from ...models.OrgInvite import org_invite_schema
from ...client_models.org_invite import OrgInviteClient
from ...constants.roles import org_roles, channel_roles
from ...models.Org import OrgSchema, Org

@main.route("/org/invite", methods=["POST"])
@login_required
def invite_to_org():
    """    
    [action: GET] - retrives all outstanding invitations for a user where user is the receipient of an invite
    Request Body: "action"
    DB tables: "org_invites"
    [action: STORE] - stores an org invite in the database if user does not already have an active invite to this org
    Request Body: "action", "orgName", "email" 
    DB tables: "org_invites"
    """
    response = {}
    data = request.json
    action = data["action"]
    if action == "GET":
        user = current_user
        org_invites = org_service.get_active_received_org_invites(user.username)
        print('ORG_INVITES', org_invites)
        org_invites_client = org_service.populate_org_invites_client(org_invites)
        print('ORG_INVITES_CLIENT', org_invites_client)
        response["org_invites"] = json.dumps(org_invites_client)
        return response
    elif action == "STORE":
        response = {}
        org_name = data["orgName"]
        org = org_service.get_org(org_name)
        inviter = current_user
        email = data["email"]
        if org_service.has_active_org_invite(org.org_id, email):
            response["ERROR"] = "User already has an active invite to this org"
            return response
        org_invite = org_service.create_org_invite(inviter, org, email)
        org_service.store_org_invite(org_invite)
        # inform connected client that they've received an org invite
        client = client_service.get_client(email)
        socket_service.send(client, "invited-to-org", org_name)
        response["successful"] = True
        return response

@main.route("/org/invite-response", methods=["POST"])
@login_required
def org_invite_response():
    """
    [POST] - marks an org_invite as responded in the database. If isAccepted is True, adds the user to the org and adds them to all public channels in the org
    Request Body: "orgName", "isAccepted"
    DB tables: "org_invites", "org_members", "channel_members"
    """
    data = request.json
    org = org_service.get_org(data["orgName"])
    user = current_user
    is_accepted = data["isAccepted"]
    org_invite = org_service.get_active_org_invite(org.org_id, user.username)
    org_service.mark_org_invite_responded(org_invite)
    if is_accepted:
        org.members.append(user)
        public_channels = list(filter(lambda c: not c.is_private, org.channels))
        for channel in public_channels:
            channel.members.append(user)
        db.session.commit()
        # get roles
        default_org_role, default_channel_role = role_service.get_role(org_roles.TADPOLE), role_service.get_role(channel_roles.TADPOLE)
        # org members role update        
        statement = role_service.gen_org_members_role_update(org.org_id, user.user_id, default_org_role.role_id)
        db.session.execute(statement)
        # channel members role update
        channel_ids = map(lambda channel: channel.channel_id, public_channels)
        statement = role_service.gen_channel_members_role_update_by_channel_ids(channel_ids, user.user_id, default_channel_role.role_id)
        db.session.execute(statement)
        db.session.commit()
        # inform connected client that they've been added to a new org
        client = client_service.get_client(user.username)
        socket_service.send(client, "added-to-org", org.name)
        permission_service.notify_permissions_updated(user.username)
    else:
        db.session.commit()
    response = {"successful": True}
    return response

# EXAMPLES
@main.route("/org/member/", methods=["GET"])
def get_org_members():
    """
    [GET] - grabs a org's org members from the DB and returns it as a JSON response (note that the OrgMember is a join of multiple tables - see OrgMember schema)
    Path: /org/member/?org_id
    Response Body: "org_members"
    DB tables: "users", "org_members", "roles"
    """
    org_id = request.args.get("org_id")
    response = {}
    if org_id is None:
        response["ERROR"] = "Missing org_id in route"
        return response
    org_members = db.session.query(OrgMember).filter_by(org_id=org_id).all()
    response["org_members"] = org_member_schema.dumps(org_members, many=True)
    return response


@main.route("/orgs", methods=[ "POST", "DELETE"])
@login_required
def orgs():
    """    
    [action: GET] - retrieves all orgs that a user is subscribed to
    Request Body: "action"
    DB tables: "org_members"
    """
    response = {}
    data = request.json
    action = data["action"]
    if action == "GET":
        orgs = current_user.org
        orgs_json = OrgSchema(exclude=["members","channels"]).dump(orgs, many=True)
        response["orgs"] = orgs_json
        return response
    
    """    
    [action: STORE] - store an org into the database if database name is not taken
    Request Body: "action, orgName"
    Info Needed: "orgName, invites, members, channels"
    DB tables: "org_members"
    """
    elif action == "STORE":
        # org_name = data["orgName"]
        org_name = "React Slack"
        org_is_available = db.session.query(Org.name).filter(name = org_name).scalar() is None
        if channel_is_available:
            users = channel_service.get_users()#for now add all users
            channels = org_service.get_channels()#for now add all channels 
            invites = org_service.get_invites()
            return response





    # elif action == "STORE":
    #     response = {}
    #     org_name = data["orgName"]
    #     org = org_service.get_org(org_name)
    #     inviter = current_user
    #     email = data["email"]
    #     if org_service.has_active_org_invite(org.org_id, email):
    #         response["ERROR"] = "User already has an active invite to this org"
    #         return response
    #     org_invite = org_service.create_org_invite(inviter, org, email)
    #     org_service.store_org_invite(org_invite)
    #     # inform connected client that they've received an org invite
    #     client = client_service.get_client(email)
    #     socket_service.send(client, "invited-to-org", org_name)
    #     response["successful"] = True
    #     return response

    # elif request.method == "POST":
    #     data = request.json
    #     channel_info = data["channel_info"]
    #     channel_name = channel_info["name"]
    #     channel_is_available = db.session.query(
    #         Channel.name).filter_by(name=channel_name).scalar() is None
    #     if channel_is_available:
    #         members = channel_info["members"]
    #         is_private = channel_info["isPrivate"]
    #         if is_private:
    #             usersResult = channel_service.get_users_by_usernames(members)
    #             if usersResult["usernames_not_found"]:
    #                 response = {
    #                     "ERROR": "Some users were not found",
    #                     "users_not_found": usersResult["usernames_not_found"]
    #                 }
    #                 return response
    #             users = usersResult["users"]
    #         else:
    #             users = channel_service.get_users()
    #         admin_username = current_user.username
    #         org = org_service.get_org(channel_info["orgName"])
    #         channel = channel_service.create_channel(
    #             channel_name, users, is_private, admin_username, org)
    #         channel_id = channel_service.store_channel(channel)
    #         # get roles
    #         members_channel_role, admin_channel_role = role_service.get_role(
    #             channel_roles.TADPOLE), role_service.get_role(channel_roles.ADMIN)
    #         # member ids
    #         admin_user_id = current_user.user_id
    #         member_user_ids = map(lambda user: user.user_id, users)
    #         # members role update
    #         statement = role_service.gen_channel_members_role_update_by_member_ids(
    #             channel_id, member_user_ids, members_channel_role.role_id)
    #         db.session.execute(statement)
    #         # admin role update
    #         statement = role_service.gen_channel_members_role_update_by_member_ids(
    #             channel_id, [admin_user_id], admin_channel_role.role_id)
    #         db.session.execute(statement)
    #         db.session.commit()
    #         # notify that permissions were updated for these users
    #         usernames = map(lambda user: user.username, users)
    #         for username in usernames:
    #             permission_service.notify_permissions_updated(username)
    #         socketio.emit("channel-created", broadcast=True)
    #         socketio.emit("added-to-channel", channel_id, broadcast=True)
    #         response = {"successful": True, }
    #         return jsonify(response)
    #     else:
    #         response = {}
    #         response["ERROR"] = "Channel name is taken"
    #         return jsonify(response)






'''
TODO
1. GET ORG Route
2. POST ORG Route
3. DELETE ORG Route
4. Check all org tables and see what I need
5. Get an understanding of the data we need to commit
6. Check channel services and see what kind of functions i will need to create
7. work my way through every line of channels routes and make sure i understand what each is doing
8. pick out what functions i will need

flow
1. look at all the tables that channels updates and see how we gather info and how we push changes
2. pseudocode what each route will do, what tables it will update and what info it will need
3. pseudocode helper function
'''
