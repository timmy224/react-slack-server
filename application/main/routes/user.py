from flask import request, jsonify
import json
from .. import main
from ... import db
from ..services import client_service
from ...models.User import User, user_schema

@main.route("/register", methods={"POST"})
def register_user():
    username = request.args.get("username", None)
    password = request.args.get("password", None)
    response = {}
    print("username is ", username)
    print("password is ", password)
    if username  is None:
         response["ERROR"] = "Missing username in route"
         return jsonify(response)

    elif password is None:
         response["ERROR"] = "Missing password in route"
         return jsonify(response)

    username_is_available = username.lower() not in client_service.clients
    print("username_is_available is :", username_is_available)

    if username_is_available:
         data = request.json
         print("data is : ", data)
         password = data["password"]
         user = User(data["username"], user.set_password(password))
         print("user is: ", user)
                
         db.session.add(user)
         db.session.commit()

         print("SUCCESS: user data inserted into db")
         
         response["successful"] = True
         return jsonify(response)

    else:
         response["ERROR"] = "username is taken"
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

# @main.route("/user/", methods=["GET", "POST"])
# def user():
#     """
#     [GET] - Grabs the user from the DB and returns it as a JSON response
#     Path: /user/?user_id={user_id}
#     Response Body: "user"
    
#     [POST] - Inserts a user into the DB using JSON passed in as request body
#     Path: /user
#     Request Body: "username"
#     Response Body: "successful"

#     DB tables: "users"
#     """
#     if request.method == "GET":
#         user_id = request.args.get("user_id", None)
#         response = {}
#         if user_id is None:
#             response["ERROR"] = "Missing user_id in route"
#             return jsonify(response)
#         user = User.query.filter_by(user_id=user_id).one()

#         user_json = user_schema.dump(user)
#         response["user"] = user_json
#         return response
#     elif request.method == "POST":
#         data = request.json
#         user = User(data["username"])

#         db.session.add(user)
#         db.session.commit()

#         print("SUCCESS: user inserted into db")
#         response = {}
#         response["successful"] = True
#         return jsonify(response)