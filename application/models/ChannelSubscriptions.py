from .. import db

channel_subscriptions = db.Table("channel_subscriptions", 
    db.Column("channel_id", db.Integer, db.ForeignKey("channels.channel_id"), primary_key=True),
    db.Column("user_id", db.Integer, db.ForeignKey("users.user_id"), primary_key=True)
)