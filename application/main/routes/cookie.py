"""
    Note: these two routes only serve as examples/learning material. The only place they're used is the cookie demo. Flask-Login will take care of the session cookie and remember cookie automatically (we do not manually create them)
"""

from flask import request, jsonify, make_response, current_app
from .. import main

@main.route("/get-cookie", methods=["GET"])
def get_cookie():
    """
    [GET] - Returns a a response with header Set-Cookie and a cookie value. Cookie will have SameSite=None and HttpOnly attributes set. Secure attribute (HTTPS) is set to True/False depending on our configuration (development vs production)
    Path: /get-cookie
    """
    response = make_response({})
    secure_cookies = current_app.config["SECURE_COOKIES"] 
    response.set_cookie("mycookie", "I am cookie", secure=secure_cookies, httponly=True, samesite="None")
    return response

@main.route("/send-cookie", methods=["GET"])
def send_cookie():
    """
    [GET] - Simple get request to test whether the cookie was automatically attached to the client's request by the browser. We attempt to print the cookie value
    Path: /send-cookie
    """
    cookie_value = request.cookies.get("mycookie")
    print("cookie_value: ", cookie_value)
    return jsonify({})