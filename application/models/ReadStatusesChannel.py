from .. import db 

read_statuses_channel = db.Table("read_statuses_channel",
    db.Column("read_id", db.Integer, primary_key = True),
    db.Column("org_id", db.Integer, db.ForeignKey("orgs.org_id")),
    db.Column("user_id",  db.Integer, db.ForeignKey("users.user_id")),
    db.Column("channel_id", db.Integer, db.ForeignKey("channels.channel_id")),
    db.Column("read_dt", db.DateTime)
)
