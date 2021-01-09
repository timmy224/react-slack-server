from .. import db, ma
from sqlalchemy import select
from sqlalchemy.orm import column_property
from .User import User
from .ReadPrivateStatuses import read_private_statuses
    
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

read_private_status_join = db.join(User, read_private_statuses, read_private_statuses.c.receiver_id == User_alias_1.user_id_a)\
    .join(User, read_private_statuses.c.user_id == User_alias_2.user_id_b)

class ReadPrivateStatus(db.Model):
    __table__ = read_private_status_join
    read_id = db.Column(db.Integer, primary_key = True)
    read_dt = db.Column(db.DateTime)
    receiver_id = column_property(read_private_statuses.c.receiver_id, User_alias_1.user_id_a)
    user_id = column_property(read_private_statuses.c.user_id, User_alias_2.user_id_b)

class ReadPrivateMessageSchema(ma.SQLAlchemySchema):
    class Meta:
        model = ReadPrivateStatus
    read_id = ma.auto_field()
    read_dt = ma.auto_field()
    receiver_id = ma.auto_field()
    user_id = ma.auto_field()
    
read_private_status_schema = ReadPrivateStatusSchema()