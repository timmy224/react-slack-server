from .. import db, ma

class OrgInvite(db.Model):
    __tablename__ = "org_invites"
    invite_id = db.Column(db.Integer, primary_key=True)
    inviter_id = db.Column(db.Integer, db.ForeignKey("users.user_id"))
    org_id = db.Column(db.Integer, db.ForeignKey("orgs.org_id"))
    email = db.Column(db.String())
    responded = db.Column(db.Boolean(), default=False)

    def __init__(self, email):
        self.email = email
    
    def __repr__(self):
        return f"<OrgInvite invite_id={self.invite_id} inviter_id={self.inviter_id} org_id={self.org_id} email={self.email} responded={self.responded}>"

class OrgInviteSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = OrgInvite

org_invite_schema = OrgInviteSchema()