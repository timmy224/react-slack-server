from .. import db 

# read_channel_messages = db.Table("read_channel_messages",
#     db.Column("message_id", db.Integer, db.ForeignKey("messages.message_id"), primary_key=True),
#     db.Column("user_id",  db.Integer, db.ForeignKey("users.user_id")),
#     db.Column("channel_id", db.Integer, db.ForeignKey("channels.channel_id"))
# )

read_channel_statuses = db.Table("read_channel_statuses",
    db.column("read_id", db.Integer, primary_key = True),
    db.Column("read_dt", db.DateTime),
    db.Column("user_id",  db.Integer, db.ForeignKey("users.user_id")),
    db.Column("channel_id", db.Integer, db.ForeignKey("channels.channel_id"))
)
