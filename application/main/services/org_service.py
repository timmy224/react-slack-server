from ... import db
from ...models.Org import Org
from ...models.OrgInvite import OrgInvite
from ...client_models.org_invite import OrgInviteClient
from ...models.Channel import Channel
from ...models.OrgInvite import OrgInvite
from ...models.Org import Org
from ...models.User import User
from ...client_models.org import OrgClient
from ...client_models.org_member import OrgMemberClient
from ...models.Channel import channel_schema
from . import client_service

def get_org(name):
    return Org.query.filter_by(name=name).one()

def create_org_invite(inviter, org, email):
    org_invite = OrgInvite(email)
    org_invite.inviter = inviter
    org_invite.org = org
    return org_invite

def store_org_invite(org_invite):
    db.session.add(org_invite)
    db.session.commit()

def get_active_received_org_invites(email):
    return OrgInvite.query.filter_by(email=email, responded=False).all()

def populate_org_invites_client(org_invites):
    return list(map(lambda invite: OrgInviteClient(invite.org.name, invite.inviter.username).__dict__, org_invites))
    
def has_active_org_invite(org_id, email):
    return OrgInvite.query.filter_by(org_id=org_id, email=email, responded=False).scalar() is not None

def get_active_org_invite(org_id, email):
    return OrgInvite.query.filter_by(org_id=org_id, email=email, responded=False).one()

def mark_org_invite_responded(org_invite):
    org_invite.responded = True

def create_org(name, members):
    org = Org(name)
    org.members = members
    return org

def store_org(org):
    db.session.add(org)
    db.session.commit()
    db.session.refresh(org)
    org_id = org.org_id
    return org_id

def create_invites_for_invited_emails(inviter, invited_emails, org):
    for email in invited_emails:
        org_invite = OrgInvite(email)
        org_invite.inviter = inviter
        org_invite.org = org
        db.session.add(org_invite)
    db.session.commit()

def create_default_org_channel(admin_username, members, org):
    name = "General"
    is_private = False
    channel = Channel(name, admin_username, is_private)
    channel.members = members
    channel.org = org
    db.session.add(channel)
    db.session.commit()
    db.session.refresh(channel)
    return channel

def delete_org(org):
    org.members = []
    for channel in org.channels:
        channel.members = []
        db.session.delete(channel)
    for invite in org.invites:
        db.session.delete(invite)
    db.session.commit()
    db.session.delete(org)
    db.session.commit()

def populate_org_client(org):
    channels_json = channel_schema.dump(org.channels, many=True)
    members = []
    for member in org.members:
        logged_in = True if client_service.get_client(member.username) else False
        org_member_client = OrgMemberClient(member.username, logged_in)
        members.append(org_member_client.__dict__)
    return OrgClient(org.name, members).__dict__

def get_users_by_usernames(org, usernames):
    users = []
    usernames_not_found = []
    for username in usernames:
        try:
            user = next(filter(lambda user: user.username == username, org.members))
            users.append(user)
        except StopIteration:
            usernames_not_found.append(username)
    return {"users": users, "usernames_not_found": usernames_not_found}

