from .. import db, ma 

# one to many relationship
class Challenge3_model(db.Model):
    __tablename__ = "challenge_table"
    
    # set up columns
    challenge_id = db.Column(db.Integer, primary_key=True)
    week_num = db.Column(db.Integer)
    challenge_content = db.Column(db.String())

    # used to construct instances
    def __init__(self, week_num, challenge_content, test):
        self.week_num = week_num,
        self.challenge_content = challenge_content
        self.test = test

    # similar to __str__, used to print non-string types in console representation
    def __repr__(self):
            return f"<Challenge3_model challenge_id={self.challenge_id} week_num={self.week_num} challenge_content={self.challenge_content}"

# allows for serializing complex object (database object) into formatted result => we want JSON later                 
class Challenge3_Schema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Challenge3_model

challenge3_schema = Challenge3_Schema()

"""
How are Marshmallow Schema's used? 
-> see user.py for example
1) Model query is used to pull database model objects from database
2) Schema is used to serialize said model object into JSON 
3) JSON is then sent to client

SELECTIVE dumping
You may not need to output all declared fields every time you use a schema. 
You can specify which fields to output with the only parameter.

summary_schema = UserSchema(only=("name", "email"))
summary_schema.dump(user)
# {"name": "Monty", "email": "monty@python.org"}
"""
