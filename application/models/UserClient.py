from .. import db, ma

class UserClient():#instantiating a new db model
	# # no __tablename__ set since it will be the same name as the class name
	# user_id  = db.Column(db.Integer, primary_key = True)#setting the user_id column, will be populated with integers, will be this tables primary key
	# username = db.Column(db.String())#setting the username column, will be populated by strings, 

	def __init__(self,user_id, username):
	# We are setting the params for instantiating a new Challenge
		self.user_id = user_id
		self.username = username

	def __repr__(self):	# method that gets called if we pring the object
		return f"<UserClient user_id={self.user_id} username={self.username}"# We are creating a string literal

# class UserClientSchema(ma.SQLAlchemyAutoSchema):#allows us to easily convert to JSON

# 	class Meta:UserClient

# #we need to instantiate the UserClientSchema
# userClient_schema = UserClientSchema()