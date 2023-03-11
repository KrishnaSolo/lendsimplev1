# Property service code
from flask import Blueprint, jsonify

from models.property import Property
from models.event import Event

property_blueprint = Blueprint("property", __name__, url_prefix="/api/property")


@property_blueprint.route("/get_listings", methods=["GET"])
def get_listings():
    # Get all active events
    events = Event.get_active_events()

    # Get all properties with active events
    properties = []
    for event in events:
        property = Property.get_property_by_id(event.property_id)
        if property:
            properties.append(
                {
                    "id": property.id,
                    "address": property.address,
                    "price": property.price,
                    "description": property.description,
                    "start_date": event.start_date,
                    "end_date": event.end_date,
                    "target_amount": event.target_amount,
                    "amount_raised": event.amount_raised,
                }
            )

    return jsonify(properties), 200
