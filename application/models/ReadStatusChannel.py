from .. import db, ma
from sqlalchemy.orm import column_property
from .Org import Org
from .Channel import Channel
from .User import User
from .ReadStatusesChannel import read_statuses_channel
    
read_status_channel_join = db.join(Channel, read_statuses_channel, Channel.channel_id == read_statuses_channel.c.channel_id)\
    .join(User, read_statuses_channel.c.user_id == User.user_id)

class ReadStatusChannel(db.Model):
    __table__ = read_status_channel_join
    read_id = db.Column(db.Integer, primary_key = True)
    org_id = column_property(read_statuses_channel.c.user_id, Org.org_id)
    user_id = column_property(read_statuses_channel.c.user_id, User.user_id)
    channel_id = column_property(read_statuses_channel.c.channel_id, Channel.channel_id)
    read_dt = db.Column(db.DateTime)

class ReadStatusChannelSchema(ma.SQLAlchemySchema):
    class Meta:
        model = ReadStatusChannel
    read_id = ma.auto_field()
    org_id = ma.auto_field()
    user_id = ma.auto_field()
    channel_id = ma.auto_field()
    read_dt = ma.auto_field()
    
read_status_channel_schema = ReadStatusChannelSchema()