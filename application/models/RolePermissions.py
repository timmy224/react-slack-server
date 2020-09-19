from .. import db

role_permissions = db.Table("role_permissions",
    db.Column("role_id", db.Integer, db.ForeignKey("roles.role_id"), primary_key=True),
    db.Column("permission_id", db.Integer, db.ForeignKey("permissions.permission_id"), primary_key=True)
)