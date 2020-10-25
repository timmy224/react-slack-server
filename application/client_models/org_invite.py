class OrgInviteClient:
    def __init__(self, org_name, inviter):
        self.org_name = org_name
        self.inviter = inviter
    
    def __repr__(self):
        return f"<OrgInviteClient org_name={self.org_name} inviter={self.inviter}>"