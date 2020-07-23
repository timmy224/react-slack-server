from .. import db, ma

class User(db.Model):
    __tablename__ = "users"
    user_id = db.Column(db.Integer, primary_key=True)
    email= db.Column(db.String())
    username = db.Column(db.String())
    name= db.Column(db.String())
    

    def __init__(self, email, username, name):
        self.email = email
        self.username = username
        self.name = name 
    
    def __repr__(self):
        return f"<  [{self.name}] :  username: [{self.username}], Email Address:[{self.email}]> "
    
class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User

user_schema = UserSchema()