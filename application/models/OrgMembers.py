from .. import db

org_members = db.Table("org_members",
    db.Column("org_id", db.Integer, db.ForeignKey("orgs.org_id"), primary_key=True),
    db.Column("user_id", db.Integer, db.ForeignKey("users.user_id"), primary_key=True),
    db.Column("role_id", db.Integer, db.ForeignKey("roles.role_id"))
)