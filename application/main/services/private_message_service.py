
class MessageClient:
    def __init__(self, type, sender, time_sent, content):
        self.type = type
        self.sender = sender 
        self.time_sent=time_sent
        self.content=content
        

class PrivateMessageClient(MessageClient):
    def __init__( self,receiver)
        self.receiver = receiver

class ChannelMessageClient(MessageClient):
    def __init__(self,channel_id)
        self.channel_id=channel_id

# # Route code 
# private_messages = # list of messages models returned by query
# privateMessagesClient = [] # list of messages to include in response to client
# message_type = "private"
# for message in private_messages:
#     receiver = message.receiver.username # Message model has a relationship defined which gives it access to sending User model
#     sender = message.sender.username # Message model also has another relationship defined which gives it access to receiving User model 
#     ...
#     privateMessage = PrivateMessage(message_type, sender, ..., receiver)
#     privateMessagesClient.append(privateMessage)
# # Convert privateMessagesClient json and attach to response. Client expects object with "messages": [array of messages] as JSON
# (edited)