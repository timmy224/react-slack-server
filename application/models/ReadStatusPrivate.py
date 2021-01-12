from .. import db, ma
from sqlalchemy import select
from sqlalchemy.orm import column_property
from .Org import Org
from .User import User
from .ReadStatusesPrivate import read_statuses_private
    
User_alias_1 = select([
    User.user_id.label("user_id_a"),
    User.username,
    User.password_hash
]).alias()

User_alias_2 = select([
    User.user_id.label("user_id_b"),
    User.username,
    User.password_hash
]).alias()

read_status_private_join = db.join(User_alias_1, read_statuses_private, read_statuses_private.c.receiver_id == User_alias_1.c.user_id_a)\
    .join(User_alias_2, read_statuses_private.c.user_id == User_alias_2.c.user_id_b)\
    .join(Org, read_statuses_private.c.org_id == Org.org_id)

class ReadStatusPrivate(db.Model):
    __table__ = read_status_private_join
    read_id = read_statuses_private.c.read_id
    org_id = column_property(read_statuses_private.c.org_id, Org.org_id)
    user_id = column_property(read_statuses_private.c.user_id, User_alias_2.c.user_id_b)
    receiver_id = column_property(read_statuses_private.c.receiver_id, User_alias_1.c.user_id_a)
    read_dt = read_statuses_private.c.read_dt

class ReadStatusPrivateSchema(ma.SQLAlchemySchema):
    class Meta:
        model = ReadStatusPrivate
    read_id = ma.auto_field()
    org_id = ma.auto_field()
    user_id = ma.auto_field()
    receiver_id = ma.auto_field()
    read_dt = ma.auto_field()
    
read_status_private_schema = ReadStatusPrivateSchema()