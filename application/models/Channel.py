from .. import db, ma

class Channel(db.Model):
    __tablename__ = "channels"
    channel_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    users = db.relationship("User", backref="channels", secondary="channel_subscriptions", lazy=True)

    def __init__(self, name):
        self.name = name
    
    def __repr__(self):
        return f"<Channel channel_id={self.channel_id} name={self.name}>"

class ChannelSchema(ma.SQLAlchemyAutoSchema):
    users = ma.Nested("UserSchema", exclude=("channels",), many=True)

    class Meta:
        model = Channel

channel_schema = ChannelSchema()