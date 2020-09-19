from .. import db, ma

class Action(db.Model):
    __tablename__ = "actions"
    action_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())

    def __init__(self, name):
        self.name = name
    
    def __repr__(self):
        return f"<Action action_id={self.action_id} name={self.name}>"

class ActionSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Action

action_schema = ActionSchema()