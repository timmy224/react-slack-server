from ... import db
from ...models.Org import Org
from ...models.OrgInvite import OrgInvite
from ...client_models.org_invite import OrgInviteClient

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
    return list(map(lambda invite: OrgInviteClient(invite.org.name, invite.inviter.username), org_invites))
    
def has_active_org_invite(org_id, email):
    return OrgInvite.query.filter_by(org_id=org_id, email=email, responded=True).scalar() is not None


