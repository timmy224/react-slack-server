class UserClient(): 
    #formatting for sending back to client with the information we expect
    def __init__ (self, user_id, username):
        self.user_id = user_id
        self.username = username

    def __repr__(self):
        return f"<UserClient user_id={self.user_id} username={self.username}>" # what defaults to print/ representing the client model.
