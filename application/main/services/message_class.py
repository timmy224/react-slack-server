class MessageClient():
    def __init__(self, sender, sent_dt, content):
        self.sender = sender
        self.sent_dt = str(sent_dt)
        self.content = content
        
class ChannelMessageClient(MessageClient):

    def __init__(self, sender, sent_dt, content, channel_id):
        super().__init__(sender, sent_dt, content)
        self.channel_id = channel_id

    def __repr__(self):
        return f'<Sender={self.sender} sent_dt={self.sent_dt} Content={self.content} channel_id={self.channel_id}>'
    
class PrivateMessageClient(MessageClient):

    def __init__(self, sender, sent_dt, content, receiver):
        super().__init__(sender, sent_dt, content)
        self.receiver = receiver

    def __repr__(self):
        return f'<Sender={self.sender} sent_dt={self.sent_dt} Content={self.content} receiver={self.receiver}>'
