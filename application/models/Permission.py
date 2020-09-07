from .. import db, ma

class Permission(db.Model):
    __tablename__ = "permissions"
    permission_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f"<Permission permission_id={self.permission_id} name={self.name}"

class PermissionSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Permission

permission_schema = PermissionSchema()