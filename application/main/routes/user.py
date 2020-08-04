from flask import request, jsonify
import json
from .. import main
from ... import db
from ..services import client_service
from ...models.User import User, user_schema, UserSchema
from ...models.Challenge3 import challenge_schema, Challenge3
from ...models.UserClient import UserClient

@main.route("/check-username/", methods=["GET"])
def check_username():
    """
    [GET] - Checks passed in username against server-side stored active socket connetions and returns
    whether the username is available 
    Path: /check-username/
    Response Body: "isAvailable"
    """
    username = request.args.get("username", None)
    response = {}
    if username is None:
        response["ERROR"] = "Missing username in route"
        return jsonify(response)        
    username_is_available = username.lower() not in client_service.clients
    response["isAvailable"] = username_is_available
    return jsonify(response)

### DATABASE ROUTES ###

@main.route("/usernames/", methods=["GET"])
def get_users():
    """
    [GET] - Grabs the usernames from the DB and returns a list of usernames as a JSON response
    Path: /users
    Response Body: "usernames"    
    DB tables: "users"
    """
    response = {}
    results = db.session.query(User.username).all()
    usernames = [result[0] for result in results]
    usernames_json = json.dumps(usernames)
    response["usernames"] = usernames_json
    return response

### EXAMPLES ###
@main.route("/get-something/", methods=["GET"]) #API end point and method type expected
def get_challenges3():
    if request.method == "GET": #good practice in case we ever wanted to add another method
        results = Challenge3.query.all() #querying for all challenge3 objects
        challengers_json = challenge_schema.dump(results, many=True) #using our MA schema to convert them to json
        response = {}
        response["challenge3"] = challengers_json
        return response

@main.route("/user/test-get-user/", methods=["GET"])
def get_one_user():
    if request.method == "GET"
        user_id = request.args.get("user_id", None) #this allows us to set a none (hence stopping a crash if nothing is there)        
        test_user= User.query.filter_by(user_id=user_id).first() # returns the first instance of when our user_id (from client) matches our user_id (from database)
        user_json = UserSchema.dump(user) #possible channel exclusion.

        #making code readable
        json_user_id = user_json["user_id"]
        json_username = user_json["username"]
        user_client = UserClient(json_user_id, json_username)

        response = {}
        response["user"] = user_json #still need to user user_client and test it can work.
        return response 

@main.route("user/test-get-users", method=["GET"])
def get_all_users():
    if request.method == "GET":
        #query for all users in db
        users = User.query.all()
        users_client = []

        #for each user in the query above we extract the user_id , create a UserClient and then convert it to json (can only do this with dict)
        for user in users:
            user_id = user.user_id
            username = user.username
            user_client = UserClient(user_id, username)
            user_client_json = json.dumps(user_client.__dict__)
            users_client.append(user_client_json)

@main.route ("user/test-store-user/", methods=["POST"])
def test_user_post():
    if request.method == "POST"
        data = request.json #getting data from client
        username = data["username"] #extracting username we should be getting from client
        user = User(username)

        db.session.add(user)
        db.session.commit()

        response ={}
        response ["successful"] = True
        return jsonify(response)

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