from flask import request, Response, jsonify, session
from flask_login import current_user, login_user, logout_user, login_required
from flask_wtf.csrf import generate_csrf
import json
from .. import main
from ... import db
from ...models.User import User
from ...models.Channel import Channel
from sqlalchemy.orm.exc import NoResultFound

@main.route("/register", methods=["POST"])
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

        #TODO query for all channels, add all channels to user model before adding to database
        channels = Channel.query.all()
        user.channels = channels

        db.session.add(user)
        db.session.commit()  
               
        response["successful"] = True
        return jsonify(response)

    else:
        response["ERROR"] = "Username is taken"
        return jsonify(response)

@main.route("/user/usernames", methods=["GET"])
@login_required
def get_users():
    response = {}
    results = db.session.query(User.username).all()
    usernames = [result[0] for result in results]
    usernames_json = json.dumps(usernames)
    response["usernames"] = usernames_json
    return response


@main.route("/logout", methods=["POST"])
@login_required
def logout():
    data = request.json
    username = data["username"] # right now we don't use this but probably will in future
    logout_user()
    response = {}
    return response

### EXAMPLES ###

@main.route("/protected-route", methods=["GET"])
# @login_required
def protected_route():
    print("Printing current user in protected route: ", current_user.username)
    return {}

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
