from .. import db, ma

class Channel(db.Model):
    __tablename__ = "channels"
    channel_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    is_private = db.Column(db.Boolean(), default=False)
    members = db.relationship("User", backref="channels", secondary="channel_members", lazy=True)


    def __init__(self, name, is_private):
        self.name = name
        self.is_private = is_private
    
    def __repr__(self):
        return f"<Channel channel_id={self.channel_id} name={self.name} is_private={self.is_private}>"

class ChannelSchema(ma.SQLAlchemyAutoSchema):
    members = ma.Nested("UserSchema", exclude=("channels",), many=True)

    class Meta:
        model = Channel

channel_schema = ChannelSchema()