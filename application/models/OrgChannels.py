from .. import db

org_channels = db.Table("org_channels",
    db.Column("org_id", db.Integer, db.ForeignKey("orgs.org_id"), primary_key=True),
    db.Column("channel_id", db.Integer, db.ForeignKey("channels.channel_id"), primary_key=True)
)