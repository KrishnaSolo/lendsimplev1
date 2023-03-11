# Auth service code
import os
from google.auth.transport import requests
from google.oauth2 import id_token
from flask import jsonify, request, Blueprint, current_app, make_response

auth_bp = Blueprint("auth_bp", __name__)


@auth_bp.route("/login", methods=["POST"])
def login():
    token = request.json.get("token")
    try:
        idinfo = id_token.verify_oauth2_token(
            token, requests.Request(), current_app.config["GOOGLE_CLIENT_ID"]
        )
        if idinfo["iss"] not in ["accounts.google.com", "https://accounts.google.com"]:
            raise ValueError("Wrong issuer.")
        email = idinfo["email"]
        # Perform any additional authorization logic here, such as checking if the user is allowed to use the app
        return jsonify({"success": True}), 200
    except ValueError:
        return jsonify({"success": False, "error": "Invalid token"}), 401


@auth_bp.route("/logout", methods=["POST"])
def logout():
    # Perform any necessary cleanup, such as revoking the user's token
    response = make_response(jsonify({"success": True}), 200)
    response.delete_cookie("token")
    return response
