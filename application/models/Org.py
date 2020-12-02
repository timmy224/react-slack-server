from .. import db, ma

class Org(db.Model):
    __tablename__ = "orgs"
    org_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    invites = db.relationship("OrgInvite", backref="org", lazy=True)

    def __init__(self, name):
        self.name = name
    
    def __repr__(self):
        return f"<Org org_id={self.org_id} name={self.name}>"

class OrgSchema(ma.SQLAlchemyAutoSchema):
    members = ma.Nested("UserSchema", exclude=("channels", "orgs", "user_id", "password_hash"), many=True)
    channels = ma.Nested("ChannelSchema", exclude=("org", "channel_id"))

    class Meta:
        model = Org
        exclude = ("org_id",)

org_schema = OrgSchema()

