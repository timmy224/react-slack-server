from .. import db

private_messages = db.Table("private_messages", 
    db.Column("message_id", db.Integer, db.ForeignKey("messages.message_id"), primary_key=True),
    db.Column("receiver_id", db.Integer, db.ForeignKey("users.user_id"))
)