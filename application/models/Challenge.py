from .. import db, ma

class Challenge(db.Model):#instantiating a new db model
	# no __tablename__ set since it will be the same name as the class name
	challenge_id  = db.Column(db.Integer, primary_key = True)#setting the challenge_id column, will be populated with integers, will be this tables primary key
	challenge_user = db.Column(db.String())#setting the challenge_user column, will be populated by strings, 

	def __init__(self, challenge_user):
	# We are setting the params for instantiating a new Challenge
		self.challenge_user = challenge_user

	def __repr__(self):	# method that gets called if we pring the object
		return f"<Challenge challenge_id={self.challenge_id} challenge_user={self.challenge_user}"# We are creating a string literal

class ChallengeSchema(ma.SQLAlchemyAutoSchema):#allows us to easily convert to JSON

	class Meta:
		model = Challenge

#we need to instantiate the ChallengeSchema
challenge_schema = ChallengeSchema()
