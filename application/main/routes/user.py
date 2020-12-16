from flask import request, Response, jsonify, session
from flask_login import current_user, login_user, logout_user, login_required
from flask_wtf.csrf import generate_csrf
import json
from .. import main
from ... import db
from ...models.User import User
from ...models.Channel import Channel
from sqlalchemy.orm.exc import NoResultFound
from ..services import oauth_service

# import os
# from ... import client
# import requests
# from flask import redirect, request, url_for
# from ...config import config
# oauth_config = config.Config.oauth

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
        user_service.add_user_db(username, password)     
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


# OAUTH TEST

# os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

# # if current_user.is_authenticated:

# @main.route("/login/test")
# def login_test():
#     # URL needed forGoogle login
#     google_provider_cfg = oauth_service.get_google_provider_cfg()
#     auth_endpoint = google_provider_cfg["authorization_endpoint"]
#     # init oauth flow with google and scope / user info request
#     request_uri = oauth_service.get_request_uri(auth_endpoint)
#     return redirect(request_uri)

# @main.route("/login/test/callback")
# def callback():
#     # Get authorization code frokm Google
#     code = request.args.get("code")
#     # URL to hit to get tokens that allow access to user information
#     google_provider_cfg = oauth_service.get_google_provider_cfg()
#     token_endpoint = google_provider_cfg["token_endpoint"]
#     # Prepare and send a request to get tokens
#     token_url, token_headers, token_body = oauth_service.get_tokens_request(token_endpoint, code)
#     token_response = oauth_service.get_token_response(token_url, token_headers, token_body)
#     # Parse the tokens!
#     parsed_tokens = oauth_service.parse_tokens(token_response)
#     # URL to hit to get user information
#     userinfo_endpoint = google_provider_cfg["userinfo_endpoint"]
#     uri, headers, body = client.add_token(userinfo_endpoint)
#     userinfo_response = oauth_service.get_userinfo_response(uri, headers, body)
#     if userinfo_response.json().get("email_verified"):
#         user_email = userinfo_response.json()["email"]
#         user = user_service.get_user(user_email)
#         if user is None:
#             user_service.add_user_db(user_email)  
#     else:
#         return {"ERROR": "User email not available or not verified by Google."}
#     login_user(user)
#     # Send user back to homepage
#     return redirect("http://localhost:5000/")

