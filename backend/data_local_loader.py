import datetime
import random
from flask import current_app
from backend.models.property import Highlight
from backend.models.property import InvestmentType
from backend.models.property import LocationScore
from backend.models.property import Property
from backend.models.event import InvestingEvent as Event
from backend.database import db


def insert_example_data():
    # Drop db
    # db.drop_all()
    # Create LocationScore
    location_score = LocationScore(transit=80, walking=80, biking=82)

    # Create InvestmentType
    investment_type = InvestmentType(
        type="Core",
        definition="A Core investment usually requires very little management from owners and are usually occupied with tenants on long-term leases. Core investments are typically acquired and held. This type of investing is as close as one can get to passive investing when buying properties directly.",
        target="For investors looking to generate stable income with very low risk.",
    )

    # Create Property
    property_data = Property(
        name="London Apartments",
        description="Participate in the ownership of a newly renovated and fully occupied 19-unit multifamily apartment building in the Vancouver-Broadway Corridor.",
        address="7935 Kennedy Rd S, Brampton, ON L6W 0A2",
        type="Lending",
        investment_needed=100000,
        investment_gained=25000,
        image="hotel.webp",
        detailed_description="Participate in the ownership of a newly renovated and fully occupied 19-unit multifamily apartment building in the Vancouver-Broadway Corridor. \n\n Participate in the ownership of a newly renovated and fully occupied 19-unit multifamily apartment building in the Vancouver-Broadway Corridor.Participate in the ownership of a newly renovated and fully occupied 19-unit multifamily apartment building in the Vancouver-Broadway Corridor.",
        annual_yield=10.5,
        target_irr=10.5,
        ant_term=2.5,
        avg_ltv=62.2,
        location_score=location_score,
        investment_type=investment_type,
    )
    db.session.add(property_data)
    db.session.commit()
    print(property_data.id)
    # Create Highlights
    highlights_data = [
        "Features 19 residential units comprising studios, jr. one-bedrooms, one-bedrooms and two-bedrooms apartments.",
        "As of this writing, all units are fully occupied. Sought-after building in a popular location suggests consistent occupancy.",
        "Constructed in 1926. First and only renovation conducted in 2017 by Haeccity Studio Architecture.",
        "Renovations aimed to preserve the heritage elements, including hardwood floors in the hallways and signature fixtures.",
        "Plaster on lathe, inlaid oak flooring, cast iron tubs and wood panel doors were all refurbished in place. Damaged areas were removed, stored and upcycled into new installations.",
        "Preserved heritage elements include cast iron furnace doors, single-hung window weights, antique lock sets, brass doorknobs and doorbells.",
    ]
    for highlight in highlights_data:
        property_data.highlights.append(Highlight(description=highlight))

    # Create a new Event object
    new_event = Event(
        property_id=property_data.id,
        start_date=datetime.datetime.now(),
        end_date=datetime.datetime.now() + datetime.timedelta(days=30),
        target_amount=100000,
        amount_raised=25000,
        active=True,
    )

    # Add the new Event object to the database session and commit the changes
    db.session.add(new_event)
    db.session.commit()
    events = Highlight.query.all()
    for event in events:
        print(event.id, event.property_id)
