from .. import db, ma

class UserClient():#instantiating a new db model

	def __init__(self,user_id, username):
	# We are setting the params for instantiating a new Challenge
		self.user_id = user_id
		self.username = username

	def __repr__(self):	# method that gets called if we pring the object
		return f"<UserClient user_id={self.user_id} username={self.username}"# We are creating a string literal