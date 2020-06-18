from flask import request, jsonify
import json
from .. import main
from ... import db
from ..services import client_service
from ...models.User import User, user_schema, UserSchema
from ...models.Challenge import Challenge, challenge_schema, ChallengeSchema
from ...models.UserClient import UserClient


@main.route("/check-username/", methods=["GET"])
def check_username():
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
    response = {}
    results = db.session.query(User.username).all()
    usernames = [result[0] for result in results]
    print(usernames)
    usernames_json = json.dumps(usernames)
    response["usernames"] = usernames_json
    return response

### EXAMPLES ###

@main.route("/user/", methods=["GET", "POST"])
def user():
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

### CHALLENGES WEEK 3 ###

@main.route("/challenge/", methods=["POST", "GET"]) #API endpoint and the method we expect from client request
def challenge():#setting our function that will be called upon API endpoint being hit
    if request.method == "POST":#setting condition for a POST method
        data = request.json# we are setting information we are receiving from the client to a data variable
        challenge = Challenge(data["challenge_user"]) #we are instantiating a new Challenge class passing in the value for "challenge_user"

        db.session.add(challenge)#stages our transaction
        db.session.commit()#completes/commits our transaction

        print("SUCCESS: challenge inserted into db")#for us to ensure that the above code ran without a problem
        response = {}#setting our response into a dict
        response["successful"] = True#setting so our dict has a key of "successful" and a value of True
        return jsonify(response)#function needs to return something in our case it will be our response as a JSON object

    elif request.method == "GET":#setting the condition for a GET method
        challenge_id = request.args.get("challenge_id", None)#requesting the challenge_id from the client request, setting a default, setting to a var
        challenge = Challenge.query.filter_by(challenge_id=challenge_id).first()#filtering through all of our Challenge objects for the one equal to the challeng_id passed in
        challenge_json = challenge_schema.dump(challenge)#using marshmallow in order to easily turn our new Challenge object into JSON

        response = {}#setting our response into a dict
        response["challenge"] = challenge_json#setting our response so its a JSON nested object
        return response#function needs to return something in our case it will be our response 

@main.route("/challenges/", methods=["GET"])#route set for retrieving all challenges
def get_challenges(): # defining our function to be called
    challenge = Challenge.query.all() # we are quering for all our Challenge objects thus no filter_by and using .all()
    challenge_json = challenge_schema.dump(challenge, many=True) #we need the many=True arg since we will be passing in multiple challenge objects
    response = {}#setting our response into a dict
    response["challenges"] = challenge_json#setting our response so its a JSON nested object
    return response#function needs to return something in our case it will be our response 

@main.route("/test-get-user/", methods=["GET"])
def get_test_user():# defining our function to be called
    if request.method == "GET":#setting the condition for a GET method
        user_id = request.args.get("user_id", None)#requesting the user_id from the client request, setting a default, setting to a var
        user = User.query.filter_by(user_id=user_id).first()#filtering through all of our User objects for the one equal to the user_id passed in
        #user_json = user_schema.dump(user)#using marshmallow in order to easily turn our new User object into JSON
        user_json = UserSchema(exclude=["channels"]).dump(user)#this returns users without channel key, need to figure out why???

        user_id = user_json["user_id"]
        username = user_json["username"]
        userclient = UserClient(user_id, username)
        print('testing userclient:', userclient)

        response = {}#setting our response into a dict
        response["user"] = user_json#setting our response so its a JSON nested object
        return response#function needs to return something in our case it will be our response 

@main.route("/test-get-users/", methods=["GET"])
def get_test_users():# defining our function to be called
    if request.method == "GET":#setting the condition for a GET method
        users = User.query.all() # we are quering for all our User objects thus no filter_by and using .all()
        #user_json = user_schema.dump(users, many=True) #we need the many=True arg since we will be passing in multiple user objects
        users_json = UserSchema(exclude=["channels"]).dump(users, many=True)#this makes the User object into dicts which allow it to be subscriptable

        user_clients = [] # setting our new list to var user_clients
        # user_clients_dict = [] # 2nd attempt at making UserClient serializable
        # for user in users:#cant do this because User object is not subsciptable
        for user in users_json:#now the list we are looping through has subsriptable objects
            user_id = user["user_id"]#we are getting neccesary info for instantiating a new UserClient
            username = user["username"]#we are getting neccesary info for instantiating a new UserClient
            new_userclient = UserClient(user_id, username)#we instantiate a new UserClient object
            new_userclient_json = json.dumps(new_userclient.__dict__)#we turn those objects into JSON by turning the UserClient objects into dicts in order to be JSON serializable
            # new_userclient_dict = new_userclient.__dict__#2nd attempt at making new UserClient JSON serializable, would have worked if we had done json.dumps(new_userclient_dict) afterwards
            user_clients.append(new_userclient_json)#adding our new JSON UserClient objects to user_clients list
            # user_clients_dict.append(new_userclient_dict)#2nd attempt,adding UserClient dicts to user_clients_dict list
        # user_clients_json = json.dumps([ob.__dict__ for ob in user_clients])#2nd attempt at making the previous UserClient dicts JSON serializable
        # user_clients_json = json.dumps(user_clients)#1st attempt at making new UserClient objects JSON serializable
    
        response = {}#setting our response into a dict
        response["userClients"] = user_clients#setting our response so its a JSON nested object
        return response#function needs to return something in our case it will be our response 

@main.route("/test-store-user/", methods=["POST"])
def post_test_user():
    if request.method == "POST":
        data = request.json# we are setting information we are receiving from the client to a data variable
        user = User(data["username"]) #we are instantiating a new User class passing in the value for "username"

        db.session.add(user)#stages our transaction
        db.session.commit()#completes/commits our transaction

        print("SUCCESS: user inserted into db")#for us to ensure that the above code ran without a problem
        response = {}#setting our response into a dict
        response["successful"] = True#setting so our dict has a key of "successful" and a value of True
        return jsonify(response)#function needs to return something in our case it will be our response as a JSON object



"""
ON CHECK_USERNAME
    [GET] - Checks passed in username against server-side stored active socket connetions and returns
    whether the username is available 
    Path: /check-username/
    Response Body: "isAvailable"
"""
"""
ON GET_USERS
    [GET] - Grabs the usernames from the DB and returns a list of usernames as a JSON response
    Path: /users
    Response Body: "usernames"    
    DB tables: "users"
"""
"""
ON DEF_USER
    [GET] - Grabs the user from the DB and returns it as a JSON response
    Path: /user/?user_id={user_id}
    Response Body: "user"
    
    [POST] - Inserts a user into the DB using JSON passed in as request body
    Path: /user
    Request Body: "username"
    Response Body: "successful"

    DB tables: "users"
"""