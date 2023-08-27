# Event service code
from flask import Blueprint, jsonify, request, current_app as app
from datetime import datetime, timezone

from backend.models.event import InvestingEvent as Event
from backend.database import db
from backend.models.property import Property
from backend.utils.auth import token_required
from backend.utils.logging import setup_logging

logger = setup_logging()
event_bp = Blueprint("event", __name__, url_prefix="/api/events")


@event_bp.route("/", methods=["GET"])
# @record_metrics
def get_all_events():
    """
    Get a paginated list of all events, with optional filters for start and end dates.
    """
    try:
        print(f"Handling get_all_events request: {request}.")
        start_date = request.args.get("start_date")
        end_date = request.args.get("end_date")
        limit = request.args.get("limit", default=10, type=int)
        cursor_str = request.args.get("cursor", default=None)

        # Convert date strings to datetime objects if present
        if start_date:
            start_date = datetime.strptime(start_date, "%Y-%m-%d")
            start_date = start_date.replace(tzinfo=timezone.utc)
        if end_date:
            end_date = datetime.strptime(end_date, "%Y-%m-%d")
            end_date = end_date.replace(tzinfo=timezone.utc)

        cursor = cursor_str if cursor_str else None

        # Query events and properties, filtering by dates if present
        query = Event.query.filter_by(active=True)
        if start_date:
            query = query.filter(Event.start_date >= start_date)
        if end_date:
            query = query.filter(Event.end_date <= end_date)
        events = query.limit(limit).offset(cursor).all()

        # Get property information for each event
        event_data = []
        for event in events:
            property_obj = db.session.query(Property).get(event.property_id)
            if not property_obj:
                logger.error(f"Property not found for event {event.key.id()}")
                continue
            event_dict = event.to_dict()
            event_dict["property"] = property_obj.to_dict()
            event_data.append(event_dict)

        response = {"events": event_data}
        more = len(events) == limit
        if more:
            response["next_cursor"] = cursor + limit

        print(f"Finished get_listings response: {response}.")
        return jsonify(response)

    except Exception as e:
        logger.exception(f"Error getting events: {str(e)}")
        return jsonify({"error": "Unable to get events"}), 500
