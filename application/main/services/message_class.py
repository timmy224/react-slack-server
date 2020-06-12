class MessageClient():
    def __init__(self, sender, time_sent, content):
        self.sender = sender
        self.time_sent = time_sent
        self.content = content
        
class ChannelMessageClient(MessageClient):
    def __init__(self, sender, time_sent, content, channel_id):
        self.channel_id = channel_id
        MessageClient.__init__(self,sender,time_sent,content)
        

class PrivateMessageClient(MessageClient):
    def __init__(self,sender, time_sent,content, receiver):
        self.receiver = receiver
        MessageClient.__init__(self,sender,time_sent,content)