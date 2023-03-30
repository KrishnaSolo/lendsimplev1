# Property service code
from json import JSONEncoder
from typing import List
from flask import Blueprint, jsonify, current_app
from backend.utils.logging import setup_logging

from backend.models.property import Property
from backend.models.event import InvestingEvent as Event


property_blueprint = Blueprint("property", __name__, url_prefix="/api/property")


def get_active_events():
    active_events: List[Event] = Event.query.filter(Event.active == True).all()
    return active_events


class PropertyEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Property):
            return {
                "id": obj.id,
                "name": obj.name,
                "description": obj.description,
                "address": obj.address,
                "type": obj.type,
                "investmentNeeded": obj.investmentNeeded,
                "investmentGained": obj.investmentGained,
                "image": obj.image,
                "detailedDescription": obj.detailedDescription,
                "annualYeild": obj.annualYeild,
                "targetIRR": obj.targetIRR,
                "antTerm": obj.antTerm,
                "avgLTV": obj.avgLTV,
                "highlights": [h.to_dict() for h in obj.highlights],
                "locationScore": obj.locationScore.to_dict(),
                "investmentType": obj.investmentType.to_dict(),
            }
        return super().default(obj)


@property_blueprint.route("/get_listings", methods=["GET"])
def get_listings():
    # Get all active events
    print(Event.query.all())
    events = get_active_events()
    print(events)
    # Get all properties with active events
    properties = []
    for event in events:
        property: Property = Property.query.get(event.property_id)
        print(property)
        if property:
            highlights = property.highlights
            properties.append(
                {
                    "id": property.id,
                    "name": property.name,
                    "description": property.description,
                    "address": property.address,
                    "type": property.type,
                    "investment_needed": property.investment_needed,
                    "investment_gained": property.investment_gained,
                    "image": property.image,
                    "detailed_description": property.detailed_description,
                    "annual_yield": property.annual_yield,
                    "target_irr": property.target_irr,
                    "ant_term": property.ant_term,
                    "avg_ltv": property.avg_ltv,
                    "highlights": highlights[0].description,
                    "location_score": {
                        "transit": property.location_score.transit,
                        "walking": property.location_score.walking,
                        "biking": property.location_score.biking,
                    },
                    "investment_type": {
                        "type": property.investment_type.type,
                        "define": property.investment_type.definition,
                        "target": property.investment_type.target,
                    },
                    "start_date": event.start_date.strftime("%Y-%m-%d %H:%M:%S"),
                    "end_date": event.end_date.strftime("%Y-%m-%d %H:%M:%S"),
                    "target_amount": event.target_amount,
                    "amount_raised": event.amount_raised,
                }
            )

    return jsonify(properties), 200
