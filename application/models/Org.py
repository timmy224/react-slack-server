from .. import db, ma

class Org(db.model):
    __tablename__ = "orgs"
    org_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    members = db.relationship("User", secondary="org_members", backref="orgs", lazy=True)
    channels = db.relationship("Channel", secondary="channels", backref="org", lazy=True)

    def __init__(self, name):
        self.name = name
    
    def __repr__(self):
        return f"<Org org_id={self.org_id} name={self.name}>"

class OrgSchema(ma.SQLAlchemyAutoSchema):
    members = ma.Nested("UserSchema", exclude=("orgs",), many=True)
    channels = ma.Nested("ChannelSchema", exclude=("org",))

    class Meta:
        model = Org

org_schema = OrgSchema()

