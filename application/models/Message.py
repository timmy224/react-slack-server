from . import db

class Message(db.Model):
    __tablename__ = "messages"
    message_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"), nullable=False)
    content = db.Column(db.String())

    def __init__(self, user_id, content):
        self.user_id = user_id
        self.content = content
    
    def __repr__(self):
        return f"<Message message_id={self.message_id} user_id={self.user_id} content={self.content}>"
