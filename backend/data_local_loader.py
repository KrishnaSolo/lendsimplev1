import datetime
import random
from flask import current_app
from backend.models.property import Highlight
from backend.models.property import InvestmentType
from backend.models.property import LocationScore
from backend.models.property import Property
from backend.models.event import InvestingEvent as Event
from backend.database import db


def insert_example_data(data):
    # Loop through each property in the data
    for prop in data["properties"]:
        # Create LocationScore
        location_score = LocationScore(
            transit=prop["locationScore"]["transit"],
            walking=prop["locationScore"]["walking"],
            biking=prop["locationScore"]["biking"],
        )

        # Create InvestmentType
        investment_type = InvestmentType(
            type=prop["investmentType"]["type"],
            definition=prop["investmentType"].get("define", ""),
            target=prop["investmentType"]["target"],
        )

        # Create Property
        property_data = Property(
            name=prop["name"],
            description=prop["description"],
            address=prop["address"],
            type=prop["type"],
            investment_needed=prop["investmentNeeded"],
            investment_gained=prop["investmentGained"],
            image=prop["image"],
            detailed_description=prop["detailedDescription"],
            annual_yield=prop.get("annualYeild", 0),
            target_irr=prop.get("targetIRR", 0),
            ant_term=prop.get("antTerm", 0),
            avg_ltv=prop.get("avgLTV", 0),
            location_score=location_score,
            investment_type=investment_type,
        )
        db.session.add(property_data)
        db.session.commit()
        print(property_data.id)
        # Create Highlights
        for highlight in prop["highlights"]:
            property_data.highlights.append(Highlight(description=highlight))

        # Create a new Event object
        new_event = Event(
            property_id=property_data.id,
            start_date=datetime.datetime.now(),
            end_date=datetime.datetime.now() + datetime.timedelta(days=30),
            target_amount=prop["investmentNeeded"],
            amount_raised=prop["investmentGained"],
            active=True,
        )

        # Add the new Event object to the database session and commit the changes
        db.session.add(new_event)
        db.session.commit()
        events = Highlight.query.all()
        for event in events:
            print(event.id, event.property_id)
