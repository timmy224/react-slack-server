from .. import db 

read_private_statuses = db.Table("read_private_statuses",
    db.Column("read_id", db.Integer, primary_key=True),
    db.Column("read_dt", db.DateTime),
    db.Column("user_id",  db.Integer, db.ForeignKey("users.user_id")),
    db.Column("receiver_id", db.Integer, db.ForeignKey("users.user_id"))
)