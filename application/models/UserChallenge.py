

class User_Object():

    def __init__(self, name, username, email):
        self.name = name
        self.username = username
        self.email = email
    
    def __repr__(self):
        return f"<User name={self.name} username={self.username} email={self.email}>"
    
# class UserSchema(ma.SQLAlchemyAutoSchema):
#     # Uses the "exclude" argument to avoid infinite recursion 
#     channels = ma.Nested("ChannelSchema", exclude=("users",), many=True)

#     class Meta:
#         model = User

# user_schema = UserSchema()