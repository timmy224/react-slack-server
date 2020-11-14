class OrgMemberClient:
    def __init__(self, username, logged_in):
        self.username = username
        self.logged_in = logged_in
    
    def __repr__(self):
        return f"<OrgInviteClient username={self.username} logged_in={self.logged_in}>"