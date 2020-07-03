from .. import db, ma
from werkzeug.security import check_password_hash

class User(db.Model):
    __tablename__ = "users"
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String())

    def __init__(self, username):
        self.username = username 
    
    def __repr__(self):
        return f"<User user_id={self.user_id} username={self.username}>"

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
class UserSchema(ma.SQLAlchemyAutoSchema):
    # Uses the "exclude" argument to avoid infinite recursion 
    channels = ma.Nested("ChannelSchema", exclude=("users",), many=True)

    class Meta:
        model = User

user_schema = UserSchema()