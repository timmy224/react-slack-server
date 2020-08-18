from flask import request, Response, jsonify, session
from flask_login import login_user
from flask_wtf.csrf import generate_csrf
import json
from .. import main
from ...models.User import User
from sqlalchemy.orm.exc import NoResultFound

@main.route("/auth/csrf", methods=["GET"])
def get_csrf_token():
    response = {}
    response = Response("CSRF token is on response header")
    response.headers["csrf-token"] = generate_csrf()
    session.permanent = True
    return response

@main.route("/auth/login", methods=["POST"])
def login():
    
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
