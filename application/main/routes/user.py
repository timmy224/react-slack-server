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

import os
from ... import client
import requests
from flask import redirect, request, url_for
from ...config import config
oauth_config = config.Config.oauth

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


# OAUTH TEST

os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

@main.route("/")
def index_test():
    if current_user.is_authenticated:
        print("TEST", current_user)
        return (
            "<p>Hello, {}! You're logged in! Email: {}</p>"
            "<div><p>Google Profile Picture:</p>"
            '<img src="" alt="Google profile pic"></img></div>'
            '<a class="button" href="/logout">Logout</a>'.format(
                current_user.username, current_user.user_id, 
            )
        )
    else:
        return '<a class="button" href="/login/test">Google Login</a>'

def get_google_provider_cfg():
    return requests.get(oauth_config.GOOGLE_DISCOVERY_URL).json()

@main.route("/login/test")
def login_test():
    # Find out what URL to hit for Google login
    google_provider_cfg = oauth_service.get_google_provider_cfg()
    auth_endpoint = google_provider_cfg["authorization_endpoint"]
    # Use library to construct the request for Google login and provide
    # scopes that let you retrieve user's profile from Google
    request_uri = oauth_service.get_request_uri(auth_endpoint)
    return redirect(request_uri)

@main.route("/login/test/callback")
def callback():
    # Get authorization code Google sent back to you
    code = request.args.get("code")
    # Find out what URL to hit to get tokens that allow you to ask for
    # things on behalf of a user
    google_provider_cfg = oauth_service.get_google_provider_cfg()
    token_endpoint = google_provider_cfg["token_endpoint"]
    # Prepare and send a request to get tokens
    # token_url, headers, body = oauth_service.get_tokens_request(token_endpoint, code)
    # token_response = requests.post(
    #     token_url,
    #     headers=headers,
    #     data=body,
    #     auth=(oauth_config.GOOGLE_CLIENT_ID, oauth_config.GOOGLE_CLIENT_SECRET),
    # )
    token_response = oauth_service.get_tokens_request(token_endpoint, code)
    # Parse the tokens!
    client.parse_request_body_response(json.dumps(token_response.json()))
    # from Google that gives you the user's profile information,
    # including their Google profile image and email
    userinfo_endpoint = google_provider_cfg["userinfo_endpoint"]
    uri, headers, body = client.add_token(userinfo_endpoint)
    userinfo_response = requests.get(uri, headers=headers, data=body)
    # You want to make sure their email is verified.
    # The user authenticated with Google, authorized your
    # app, and now you've verified their email through Google!
    if userinfo_response.json().get("email_verified"):
        print("TEST", userinfo_response.json())
        unique_id = userinfo_response.json()["sub"]
        users_email = userinfo_response.json()["email"]
        picture = userinfo_response.json()["picture"]
        users_name = userinfo_response.json()["given_name"]
    else:
        return "User email not available or not verified by Google.", 400
    # Create a user in your db with the information provided
    # by Google
    # user = User(
    #     id_=unique_id, name=users_name, email=users_email, profile_pic=picture
    # )
    user = User(users_email)
    user.set_password(unique_id)
    db.session.add(user)
    db.session.commit() 

    # Doesn't exist? Add it to the database.
    # if not User.get(unique_id):
    #     User.create(unique_id, users_name, users_email, picture)

    # Begin user session by logging the user in
    login_user(user)

    # Send user back to homepage
    return redirect("http://localhost:5000/")

@main.route("/logout/test")
@login_required
def logout_test():
    logout_user()
    return redirect(url_for("index"))