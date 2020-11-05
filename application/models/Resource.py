from .. import db, ma

class Resource(db.Model):
    __tablename__ = "resources"
    resource_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())

    def __init__(self, name):
        self.name = name
    
    def __repr__(self):
        return f"<Resource resource_id={self.resource_id} name={self.name}>"

class ResourceSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Resource

resource_schema = ResourceSchema()