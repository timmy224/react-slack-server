from .. import db

channel_messages = db.Table("channel_messages",
    db.Column("message_id", db.Integer, db.ForeignKey("messages.message_id"), primary_key=True),
    db.Column("channel_id", db.Integer, db.ForeignKey("channels.channel_id"))
)