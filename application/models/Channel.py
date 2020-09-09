from .. import db, ma

class Channel(db.Model):
    __tablename__ = "channels"
    channel_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    admin_username = db.Column(db.String(),db.ForeignKey("users.username"))
    is_private = db.Column(db.Boolean(), default=False)
    users = db.relationship("User", backref="channels", secondary="channel_subscriptions", lazy=True)

    def __init__(self, name, admin_username, is_private):
        self.name = name
        self.admin_username = admin_username
        self.is_private = is_private
    
    def __repr__(self):
        return f"<Channel channel_id={self.channel_id} name={self.name} admin_username = {self.admin_username} is_private={self.is_private}>"

class ChannelSchema(ma.SQLAlchemyAutoSchema):
    users = ma.Nested("UserSchema", exclude=("channels",), many=True)

    class Meta:
        model = Channel

channel_schema = ChannelSchema()
