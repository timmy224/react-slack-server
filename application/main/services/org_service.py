from ... import db
from ...models.Org import Org

def get_org(name):
    org = Org.query.filter_by(name=name).one()
    return org