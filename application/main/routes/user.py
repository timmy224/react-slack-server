from flask import request, Response, jsonify
from flask_login import current_user, login_user, login_required
from flask_wtf.csrf import generate_csrf
import json
from .. import main
from ... import db
from ..services import client_service
from ...models.User import User, user_schema
from sqlalchemy.orm.exc import NoResultFound

@main.route("/register", methods={"POST"})
def register_user():
    response = {}
    data = request.json
    username, password = data["username"], data["password"]

    if username  == "":
        response["ERROR"] = "Missing username in route"
        return jsonify(response)

    elif password == "":
        response["ERROR"] = "Missing password in route"
        return jsonify(response)

    username_is_available =  db.session.query(User.user_id).filter_by(username = username).scalar() is None
    if username_is_available:
        user = User(username)
        user.set_password(password)

        db.session.add(user)
        db.session.commit()  
               
        response["successful"] = True
        return jsonify(response)

    else:
        response["ERROR"] = "Username is taken"
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


@main.route("/login", methods=["GET", "POST"])
def login():
    response = {}
    if request.method == "GET":
        response = Response("CSRF token is on response header")
        response.headers["csrf-token"] = generate_csrf()
        return response
    elif request.method == "POST":
        if request.method == "POST":
            data = request.json
            username = data["username"]
            password = data["password"]
            if username is None or password is None:
                response["ERROR"] = "Missing username"
                return jsonify(response)
            try: 
                user = User.query.filter_by(username=username).one()
            except NoResultFound:
                response= {}
                response["ERROR"] = "Wrong credentials"
                return jsonify(response)
            is_correct_password = user.check_password(password)
            if not is_correct_password:
                response= {}
                response["ERROR"] = "Wrong credentials"
                return jsonify(response)
            login_user(user, remember=True)
            response = {}
            response["isAuthenticated"] = True
            return jsonify(response)

### EXAMPLES ###

@main.route("/protected-route", methods=["GET"])
@login_required
def protected_route():
    print("Printing current user in protected route: ", current_user.username)
    return {}

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