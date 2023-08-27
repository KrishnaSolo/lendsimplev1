# Investor service code
from flask import Blueprint, request, jsonify, current_app as app
from werkzeug.exceptions import BadRequest

from backend.models.investor import Investor
from backend.database import db
from backend.utils.logging import record_execution_time

investor_bp = Blueprint("investor", __name__, url_prefix="/api/investor")


@investor_bp.route("/new", methods=["POST"])
@record_execution_time
def create_investor():
    try:
        app.logger.info(f"Handling create_investor request:{request}.")
        data = request.get_json()
        if not data:
            raise BadRequest("No data provided")
        investor = Investor(**data)
        db.session.add(investor)
        res = db.session.commit()
        app.logger.info(f"Added investor to DB: {res}")
        return jsonify(investor.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        raise e


@investor_bp.route("/<investor_id>", methods=["GET"])
@record_execution_time
def get_investor(investor_id):
    app.logger.info(f"Handling get_investor request: {investor_id}, {request}.")
    investor = Investor.query.get(investor_id)
    if not investor:
        raise BadRequest(f"Investor with ID {investor_id} not found")
    app.logger.info(f"Found investor: {investor}")
    return jsonify(investor.to_dict())


@investor_bp.route("/admin/", methods=["GET"])
@record_execution_time
def get_all_investors():
    investors = Investor.query.all()
    if not len(investors):
        raise BadRequest(f"Investors not found")
    return jsonify([investor.to_dict() for investor in investors])


@investor_bp.route("/<investor_id>", methods=["PUT"])
@record_execution_time
def update_investor(investor_id):
    try:
        investor = Investor.query.get(investor_id)
        if not investor:
            raise BadRequest(f"Investor with ID {investor_id} not found")
        data = request.get_json()
        if not data:
            raise BadRequest("No data provided")
        investor.update(**data)
        db.session.commit()
        return jsonify(investor.to_dict())
    except Exception as e:
        db.session.rollback()
        raise e


@investor_bp.route("/<investor_id>", methods=["DELETE"])
@record_execution_time
def delete_investor(investor_id):
    try:
        investor = Investor.query.get(investor_id)
        if not investor:
            raise BadRequest(f"Investor with ID {investor_id} not found")
        db.session.delete(investor)
        db.session.commit()
        return "", 204
    except Exception as e:
        db.session.rollback()
        raise e
