from flask import request, Response, jsonify
from flask_login import current_user, login_user, login_required
from flask_wtf.csrf import generate_csrf
import json
from .. import main
from ... import db
from ...models.User import User
from ...models.Channel import Channel
from sqlalchemy.orm.exc import NoResultFound

@main.route("/register/post", methods=["POST"])
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
def get_users():
    response = {}
    results = db.session.query(User.username).all()
    usernames = [result[0] for result in results]
    usernames_json = json.dumps(usernames)
    response["usernames"] = usernames_json
    return response


@main.route("/auth/csrf", methods=["GET"])
def get_login():
    response = {}
        response = Response("CSRF token is on response header")
        response.headers["csrf-token"] = generate_csrf()
        return response

@main.route("/auth/login", methods=["POST"])
def post_login():
    
    data = request.json
    username = data["username"]
    password = data["password"]
    if username is None or password is None:
        response["ERROR"] = "Missing username"
        return jsonify(response)
    try: 
        user = User.query.filter_by(username=username).one()
        is_correct_password = user.check_password(password)
        if not is_correct_password:
            response = {}
            response["ERROR"] = "Wrong credentials"
            return jsonify(response)
        login_user(user, remember=True)
        response = {}
        response["isAuthenticated"] = True
        return jsonify(response)
    except NoResultFound:
        response= {}
        response["ERROR"] = "Wrong credentials"
        return jsonify(response)

### EXAMPLES ###

@main.route("/protected-route", methods=["GET"])
# @login_required
def protected_route():
    print("Printing current user in protected route: ", current_user.username)
    return {}
