import jwt
from functools import wraps
from flask import request, jsonify
from ..models.investor import Investor
from ..config import Config


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        if "x-access-token" in request.headers:
            token = request.headers["x-access-token"]

        if not token:
            return jsonify({"message": "Token is missing"}), 401

        try:
            data = jwt.decode(token, Config.SECRET_KEY)
            investor = Investor.query.filter_by(id=data["id"]).first()
        except:
            return jsonify({"message": "Token is invalid"}), 401

        return f(investor, *args, **kwargs)

    return decorated
