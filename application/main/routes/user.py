from flask import request, jsonify
from .. import main
from ... import db
from ..services import client_service
from ...models.User import User, UserSchema, user_schema


@main.route("/check-username/", methods=["GET"])
def check_username():
    """
    [GET] - Checks passed in username against server-side stored active socket connetions and returns
    whether the username is available 
    Path: /check-username/
    Response Body: "isAvailable"
    """
    username = request.args.get("username", None)
    print(f"Checking username: {username}")

    response = {}
    if username is None:
        response["ERROR"] = "Missing username in route"
        return jsonify(response)        
    username_is_available = username.lower() not in client_service.clients
    response["isAvailable"] = username_is_available
    return jsonify(response)

### DATABASE ROUTES ###

@main.route("/users/", methods=["GET"])
def get_users():
    """
    [GET] - Grabs the users from the DB and returns a list of user objects (each containing a username) as a JSON response
    Path: /users
    Response Body: "users"    
    DB tables: "users"
    """
    response = {}
    users = User.query.all()
    users_json = UserSchema(only=["username"]).dump(users, many=True)
    response["users"] = users_json
    return response

### EXAMPLES ###

@main.route("/user/", methods=["GET", "POST"])
def user():
    """
    [GET] - Grabs the user from the DB and returns it as a JSON response
    Path: /user/?user_id={user_id}
    Response Body: "user"
    
    [POST] - Inserts a user into the DB using JSON passed in as request body
    Path: /user
    Request Body: "username"
    Response Body: "successful"

    DB tables: "users"
    """
    if request.method == "GET":
        user_id = request.args.get("user_id", None)
        response = {}
        if user_id is None:
            response["ERROR"] = "Missing user_id in route"
            return jsonify(response)
        user = User.query.filter_by(user_id=user_id).one()

        user_json = user_schema.dump(user)
        response["user"] = user_json
        return response
    elif request.method == "POST":
        data = request.json
        user = User(data["username"])

        db.session.add(user)
        db.session.commit()

        print("SUCCESS: user inserted into db")
        response = {}
        response["successful"] = True
        return jsonify(response)