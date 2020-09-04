from .. import db, ma

class Role(db.Model):
    __tablename__ = "roles"
    role_id = db.Column(db.Integer, primary_key=True),
    name = db.Column(db.String())

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f"<Role role_id={self.role_id} name={self.name}"

class RoleSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Role

role_schema = RoleSchema()