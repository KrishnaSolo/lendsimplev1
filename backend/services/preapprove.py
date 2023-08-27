# Preapprove service code
from flask import Blueprint, request, jsonify, current_app as app
from backend.services.flinks_service import FlinksService

from backend.models.investor import Investor
from backend.models.event import InvestingEvent as Event
from backend.utils.logging import record_execution_time, setup_logging

pre_approve_bp = Blueprint("pre_approve_bp", __name__)

logger = setup_logging()


@pre_approve_bp.route("/pre-approve", methods=["POST"])
# @metric_decorator
@record_execution_time
def pre_approve():
    """
    Check if investor has enough balance to invest without exceeding target amount.
    """
    app.logger.info(f"Handling pre_approve request:{request}.")
    data = request.get_json()

    investor_id = data.get("investor_id")
    event_id = data.get("event_id")
    amount = float(data.get("amount"))

    investor = Investor.get_by_id(investor_id)
    event = Event.get_by_id(event_id)

    if not investor:
        logger.warning(f"Investor with id {investor_id} does not exist.")
        return (
            jsonify(
                {
                    "success": False,
                    "message": f"Investor with id {investor_id} does not exist.",
                }
            ),
            404,
        )

    if not event:
        logger.warning(f"Event with id {event_id} does not exist.")
        return (
            jsonify(
                {
                    "success": False,
                    "message": f"Event with id {event_id} does not exist.",
                }
            ),
            404,
        )

    # check if amount is within target amount
    if event.amount_raised + amount > event.target_amount:
        logger.warning(f"Investment amount exceeds target amount for event {event_id}.")
        return (
            jsonify(
                {
                    "success": False,
                    "message": f"Investment amount exceeds target amount for event {event_id}.",
                }
            ),
            400,
        )

    # check if investor has enough balance to invest
    bank_accnt_id = investor.bank_account_id
    if FlinksService.check_balance(bank_accnt_id, amount):
        logger.warning(
            f"Investor {investor_id} does not have enough balance to invest ${amount}."
        )
        return (
            jsonify(
                {
                    "success": False,
                    "message": f"Investor {investor_id} does not have enough balance to invest ${amount}.",
                }
            ),
            400,
        )

    # add investor to approval queue
    approval_queue = request.approval_queue
    approval_queue.put(
        {"investor_id": investor_id, "event_id": event_id, "amount": amount}
    )

    app.logger.info(
        f"Investor {investor_id} pre-approved for investing ${amount} in event {event_id}."
    )
    return (
        jsonify(
            {
                "success": True,
                "message": f"Investor {investor_id} pre-approved for investing ${amount} in event {event_id}.",
            }
        ),
        200,
    )
