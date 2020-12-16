from ... import client
import requests
from flask import redirect, request, url_for
from ...config import config
oauth_config = config.Config.oauth
import json

def get_google_provider_cfg():
    return requests.get(oauth_config.GOOGLE_DISCOVERY_URL).json()

def get_request_uri(auth_endpoint):
    request_uri =  client.prepare_request_uri(
            auth_endpoint,
            redirect_uri="http://localhost:3000/auth/login-google/callback",
            scope=["email"],
        )
    return request_uri

def get_tokens_request(token_endpoint, code):
    token_url, headers, body = client.prepare_token_request(
        token_endpoint,
        authorization_response=request.url,
        redirect_url=request.base_url,
        code=code
        )
    return token_url, headers, body

def get_token_response(token_url, headers, body):
    token_response = requests.post(
        token_url,
        headers=headers,
        data=body,
        auth=(oauth_config.GOOGLE_CLIENT_ID, oauth_config.GOOGLE_CLIENT_SECRET),
    )
    return token_response

def parse_tokens(token_response):
    return client.parse_request_body_response(json.dumps(token_response.json()))

def get_userinfo_response(uri, headers, body):
    response = requests.get(uri, headers=headers, data=body)
    return response
    