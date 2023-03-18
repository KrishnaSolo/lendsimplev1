# Investor service code
from flask import Blueprint, request, jsonify
from werkzeug.exceptions import BadRequest

from backend.models.investor import Investor
from backend.database import db
from backend.utils.logging import record_execution_time

investor_bp = Blueprint("investor", __name__, url_prefix="/api/investor")


@investor_bp.route("/", methods=["POST"])
@record_execution_time
def create_investor():
    try:
        data = request.get_json()
        if not data:
            raise BadRequest("No data provided")
        investor = Investor(**data)
        db.session.add(investor)
        db.session.commit()
        return jsonify(investor.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        raise e


@investor_bp.route("/<investor_id>", methods=["GET"])
@record_execution_time
def get_investor(investor_id):
    investor = Investor.query.get(investor_id)
    if not investor:
        raise BadRequest(f"Investor with ID {investor_id} not found")
    return jsonify(investor.to_dict())


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


@investor_bp.route("/", methods=["GET"])
@record_execution_time
def get_all_investors():
    investors = Investor.query.all()
    return jsonify([investor.to_dict() for investor in investors])
