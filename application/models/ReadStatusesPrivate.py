from .. import db 

read_statuses_private = db.Table("read_statuses_private",
    db.Column("read_id", db.Integer, primary_key=True),
    db.Column("org_id", db.Integer, db.ForeignKey("org.org_id")),
    db.Column("user_id",  db.Integer, db.ForeignKey("users.user_id")),
    db.Column("receiver_id", db.Integer, db.ForeignKey("users.user_id")),
    db.Column("read_dt", db.DateTime)
)