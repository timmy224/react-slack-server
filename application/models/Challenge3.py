from .. import db, ma 

class Challenge3(db.Model):
    challenge_id = db.Column(db.Integer, primary_key=True)
    challenge = db.Column(db.String())

    def __init__(self, challenge):
        self.challenge = challenge 
    
    def __repr__(self):
        return f"<Challnege3 challenge_id={self.challenge_id} challenge={self.challenge}>"
    
class ChallengeSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Challenge3

challenge_schema = ChallengeSchema()