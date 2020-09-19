from .. import db

channel_members = db.Table("channel_members", 
    db.Column("channel_id", db.Integer, db.ForeignKey("channels.channel_id"), primary_key=True),
    db.Column("user_id", db.Integer, db.ForeignKey("users.user_id"), primary_key=True),
    db.Column("role_id", db.Integer, db.ForeignKey("roles.role_id"), primary_key=True)
)