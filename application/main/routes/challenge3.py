from flask import request
from ...models.challenge3_model import Challenge3_model, challenge3_schema
from ...models.User import User, user_schema
from .. import main
from ... import db
import json

### Creating challenge 3 routes here for easier cleanup later

@main.route("/get-something/", methods=["GET"])
def challenge3_get_something():
    if request.method == "GET":
        challenge3_output = Challenge3_model.query.all()
        print(challenge3_output)

        challenge3_json = challenge3_schema.dump(challenge3_output, many=True)
        print(challenge3_json)

        response = {}
        response['data'] = challenge3_json
        return response
    
@main.route("/test-get-users/", methods=["GET"])
def challenge3_get_users():
    if request.method == "GET":
        test_user = User.query.all()
        print(test_user)

        test_user_json = user_schema.dump(test_user, many=True)
        print(test_user_json)

        response = {}
        response['users'] = test_user_json
        return response

@main.route("/test-store-user/", methods=["POST"])
def challenge3_add_username():
    if request.method == "POST":
        data = request.json # post data is JSON.stringified and added to post body
        username = data.get("username") # returns default of None if key not found

        new_user = User(username)
        db.session.add(new_user)
        db.session.commit()

        response = {}
        response['successful'] = True
        return response


@main.route("/test-get-users-2/", methods=["GET"])
def challenge3_get_users_2():
    class UserClient:
        def __init__(self, user_id, username):
            self.user_id = user_id
            self.username = username

        def __repr__(self):
            return f"<UserClient user_id={self.user_id} username={self.username}>"

    if request.method == "GET":
        test_users = User.query.all()
        
        user_clients = []
        for user in test_users:
            new_user = UserClient(user.user_id, user.username)
            user_clients.append(new_user)

        user_dicts = [user.__dict__ for user in user_clients]
        data = json.dumps(user_dicts)
        response = {}
        response['users'] = data

        print(response)
        return response
