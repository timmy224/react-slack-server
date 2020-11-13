class OrgClient:
    def __init__(self, org_name, channels, members):
        self.name = org_name
        self.channels = channels
        self.members = members
    
    def __repr__(self):
        return f"<OrgClient org_name={self.org_name} channels={self.channels} members={self.members}>"