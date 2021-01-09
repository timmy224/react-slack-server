from .. import main
from ..services import user_service, status_service

@main.route("/status/read", methods=['POST'])
def get_statuses() => response:
    """ gets channel and private read statuses """
    data = request.json()
    username = current_user.username
    user_id = user_service.get_user(username).user_id
    private_statuses = status_service.get_private_statuses(username)
    channel_statuses = status_service.get_channel_statuses(username)
    statuses = {
        "channel_statuses": channel_statuses, 
        "private_statuses": private_statuses
    }
    # TODO confirm dict structure 
    response['read_statuses'] = json.dumps(statuses)
    return response

#NOTE will need to account for table clean up i.e. when channels / private messages get deleted