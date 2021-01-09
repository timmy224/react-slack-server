from ... import db
from . import user_service
from ...models.ReadChannelStatus import ReadChannelStatus
from ...models.ReadChannelStatuses import read_channel_statuses
from ...models.ReadPrivateStatus import ReadPrivateStatus
from ...models.ReadPrivateStatuses import read_private_statuses

def get_read_channel_statuses(user_id) -> dict:
    """ gets read datetime for channel statuses from db """
    channel_statuses = db.session.query(ReadChannelStatus).filter_by(user_id=user_id).all()
    return channel_statuses

def get_read_private_statuses(user_id) -> dict:
    """ gets read datetime for private statuses from db """
    private_statuses = db.session.query(ReadPrivateStatus).filter_by(user_id=user_id).all()
    return private_statuses

def set_read_channel_status(user_id, channel_id, read_dt):
    """ sets read datetime for specific channel in db """
    channel_status_exists = db.session.query(db.exists().filter_by(
            ReadChannelStatus.user_id == user_id,
            ReadChannelStatus.channel_id == channel_id
        )).scalar()
    if channel_status_exists:
        channel_status = db.session.query(db.exists().filter_by(
            ReadChannelStatus.user_id == user_id,
            ReadChannelStatus.channel_id == channel_id
        )).one()
        channel_status.read_dt = read_dt
    else:
        new_channel_status = ReadChannelStatus(user_id = user_id, channel_id = channel_id, read_dt = read_dt)
        db.session.add(new_channel_status)
    db.session.commit()

def set_read_private_status(user_id, receiver_id, read_dt):
    """ sets read datetime for specific private message room in db """
    private_status_exists = db.session.query(db.exists().filter_by(
            ReadPrivateStatus.user_id == user_id,
            ReadPrivateStatus.receiver_id == receiver_id
        )).scalar()
    if private_status_exists:
        private_status = db.session.query(db.exists().filter_by(
            ReadPrivateStatus.user_id == user_id,
            ReadPrivateStatus.receiver_id == channel_id
        )).one()
        private_status.read_dt = read_dt
    else:
        new_private_status = ReadPrivateStatus(user_id = user_id, receiver_id = receiver_id, read_dt = read_dt)
        db.session.add(new_private_status)
    db.session.commit()