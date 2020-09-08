from .. import db

permissions = db.Table("permissions",
    db.Column("permission_id", db.Integer, primary_key=True),
    db.Column("resource_id", db.Integer, db.ForeignKey("resources.resource_id")),
    db.Column("action_id", db.Integer, db.ForeignKey("actions.action_id"))
)