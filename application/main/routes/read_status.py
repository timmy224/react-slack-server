from .. import main
from ..services import user_service, read_status_service

@main.route("/status/read", methods=['POST'])
def get_statuses():
    """ gets channel and private read statuses """
    data = request.json()
    username = current_user.username
    read_statuses = read_status_service.get_statuses(username)
    response['read_statuses'] = json.dumps(read_statuses)
    return response
