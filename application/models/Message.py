from .. import db

class Message(db.Model):
    __tablename__ = "messages"
    message_id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer, db.ForeignKey("users.user_id"), nullable=False)
    sent_dt = db.Column(db.DateTime)
    content = db.Column(db.String())
    sender = db.relationship("User", backref="sent_messages", lazy=True)
    receiver = db.relationship("User", secondary="private_messages", backref="received_messages", uselist=False, lazy=True)
    channel = db.relationship("Channel", secondary="channel_messages", backref="messages", uselist=False, lazy=True)

    def __init__(self, sender_id, sent_dt, content):
        self.sender_id = sender_id
        self.sent_dt = sent_dt
        self.content = content
    
    def __repr__(self):
        return f"<Message message_id={self.message_id} user_id={self.user_id} content={self.content}>"
