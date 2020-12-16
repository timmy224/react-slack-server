from flask import request, Response, jsonify, session, redirect
from flask_login import login_user
from flask_wtf.csrf import generate_csrf
import json
from .. import main
from ...models.User import User
from sqlalchemy.orm.exc import NoResultFound

import os
from ... import client

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

os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

@main.route("/login-google", methods=["GET"])
def google_login():
    # URL needed forGoogle login
    google_provider_cfg = oauth_service.get_google_provider_cfg()
    auth_endpoint = google_provider_cfg["authorization_endpoint"]
    # init oauth flow with google and scope / user info request
    request_uri = oauth_service.get_request_uri(auth_endpoint)
    return redirect(request_uri)

@main.route("/login-google/callback")
def callback():
    # Get authorization code from Google
    code = request.args.get("code")
    # URL to hit to get tokens that allow access to user information
    google_provider_cfg = oauth_service.get_google_provider_cfg()
    token_endpoint = google_provider_cfg["token_endpoint"]
    # Prepare and send a request to get tokens
    token_url, token_headers, token_body = oauth_service.get_tokens_request(token_endpoint, code)
    token_response = oauth_service.get_token_response(token_url, token_headers, token_body)
    parsed_tokens = oauth_service.parse_tokens(token_response)
    # URL to hit to get user information
    userinfo_endpoint = google_provider_cfg["userinfo_endpoint"]
    uri, headers, body = client.add_token(userinfo_endpoint)
    userinfo_response = oauth_service.get_userinfo_response(uri, headers, body)
    if userinfo_response.json().get("email_verified"):
        user_email = userinfo_response.json()["email"]
        user = user_service.get_user(user_email)
        if user is None:
            user_service.add_user_db(user_email)  
    else:
        response = {"ERROR": "User email not available or not verified by Google."}
        return jsonify(response)
    login_user(user, remember=True)
    response = {}
    response["isAuthenticated"] = True
    response["username"] = user_email
    return jsonify(response)

