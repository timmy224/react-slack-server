class OrgClient:
    def __init__(self, org_name, members):
        self.name = org_name
        self.members = members
    
    def __repr__(self):
        return f"<OrgClient org_name={self.name} members={self.members}>"