from .. import db, ma
from sqlalchemy.orm import column_property
from .Channel import Channel
from .User import User
from .ReadChannelStatuses import read_channel_statuses
    
read_channel_status_join = db.join(Channel, read_channel_statuses, Channel.channel_id == read_channel_statuses.c.channel_id)\
    .join(User, read_channel_statuses.c.user_id == User.user_id)

class ReadChannelStatus(db.Model):
    __table__ = read_channel_status_join
    read_id = db.Column(db.Integer, primary_key = True)
    read_dt = db.Column(db.DateTime)
    channel_id = column_property(read_channel_statuses.c.channel_id, Channel.channel_id)
    user_id = column_property(read_channel_statuses.c.user_id, User.user_id)

class ReadChannelStatusSchema(ma.SQLAlchemySchema):
    class Meta:
        model = ReadChannelStatus
    read_id = ma.auto_field()
    read_dt = ma.auto_field()
    channel_id = ma.auto_field()
    user_id = ma.auto_field()
    
read_channel_status_schema = ReadChannelStatusSchema()