from ... import db
from . import user_service, org_service, channel_service
from ...models.ReadStatusChannel import ReadStatusChannel
from ...models.ReadStatusesChannel import read_statuses_channel
from ...models.ReadStatusPrivate import ReadStatusPrivate
from ...models.ReadStatusesPrivate import read_statuses_private

def get_read_statuses_channel(user_id) -> dict:
    """ gets read datetime for channel statuses from db """
    channel_statuses = ReadStatusChannel.query.filter_by(user_id=user_id).all()
    return channel_statuses

def get_read_private_statuses(user_id) -> dict:
    """ gets read datetime for private statuses from db """
    private_statuses = ReadStatusPrivate.query.filter_by(user_id=user_id).all()
    return private_statuses

def set_read_status_channel(read_status):
    """ sets read datetime for specific channel in db """
    org_name = read_status["org_name"]
    org_id = org_service.get_org(org_name).org_id
    channel_name = read_status["channel_name"]
    channel_id = channel_service.get_channel(org_name, channel_name).channel_id
    user_id = user_service.get_user(username).user_id
    read_dt = read_status["read_dt"]
    channel_status = ReadStatusChannel.query.filter_by(
            org_id=org_id,
            user_id=user_id,
            channel_id=channel_id
        )).first()
    if not channel_status:      # channel does not exist
        new_channel_status = ReadStatus(user_id = user_id, org_id = org_id, channel_id = channel_id, read_dt = read_dt)
        db.session.add(new_channel_status)
    else:                       # channel does exist
        channel_status.read_dt = read_dt
    db.session.commit()

def set_read_status_private(read_status):
    """ sets read datetime for specific private message room in db """
    org_name = read_status["org_name"]
    org_id = org_service.get_org(org_name).org_id
    receiver_username = read_status['receiver_username']
    receiver_id = user_service.get_user(receiver_username).user_id
    user_id = user_service.get_user(username).user_id
    read_dt = read_status["read_dt"]
    private_status = ReadStatusPrivate.query.filter_by(
            org_id=org_id,
            user_id=user_id,
            receiver_id=receiver_id
        )).first()
    if not private_status:
        new_private_status = ReadStatusPrivate(user_id = user_id, org_id = org_id, receiver_id = receiver_id, read_dt = read_dt)
        db.session.add(new_private_status)
    else:
        private_status.read_dt = read_dt
    db.session.commit()

def get_statuses(username):
    statuses = {
        "channel_statuses": get_read_statuses_channel(username), 
        "private_statuses": get_read_statuses_private(username)
    }
    return statusess