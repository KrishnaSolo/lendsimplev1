# Property model code
from backend.database import db


class Property(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, unique=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    address = db.Column(db.String(200), nullable=False)
    type = db.Column(db.String(50), nullable=False)
    investment_needed = db.Column(db.Float, nullable=False)
    investment_gained = db.Column(db.Float, nullable=False)
    image = db.Column(db.String(100), nullable=False)
    detailed_description = db.Column(db.Text, nullable=False)
    annual_yield = db.Column(db.Float, nullable=False)
    target_irr = db.Column(db.Float, nullable=False)
    ant_term = db.Column(db.Float, nullable=False)
    avg_ltv = db.Column(db.Float, nullable=False)

    highlights = db.relationship("Highlight", backref="property")
    location_score_id = db.Column(
        db.Integer, db.ForeignKey("location_score.id"), nullable=False
    )
    location_score = db.relationship("LocationScore", back_populates="properties")
    investment_type_id = db.Column(
        db.Integer, db.ForeignKey("investment_type.id"), nullable=False
    )
    investment_type = db.relationship("InvestmentType", back_populates="properties")

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "address": self.address,
            "type": self.type,
            "investment_needed": self.investment_needed,
            "investment_gained": self.investment_gained,
            "image": self.image,
            "detailed_description": self.detailed_description,
            "annual_yield": self.annual_yield,
            "target_irr": self.target_irr,
            "ant_term": self.ant_term,
            "avg_ltv": self.avg_ltv,
            "highlights": [highlight.description for highlight in self.highlights],
            "location_score": {
                "transit": self.location_score.transit,
                "walking": self.location_score.walking,
                "biking": self.location_score.biking,
            },
            "investment_type": {
                "type": self.investment_type.type,
                "definition": self.investment_type.definition,
                "target": self.investment_type.target,
            },
        }


class Highlight(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.Text, nullable=False)
    property_id = db.Column(db.Integer, db.ForeignKey("property.id"), nullable=False)

    def to_dict(self):
        return {"id": self.id, "description": self.description}


class LocationScore(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    transit = db.Column(db.Integer, nullable=False)
    walking = db.Column(db.Integer, nullable=False)
    biking = db.Column(db.Integer, nullable=False)

    properties = db.relationship("Property", back_populates="location_score")

    def to_dict(self):
        return {
            "id": self.id,
            "transit": self.transit,
            "walking": self.walking,
            "biking": self.biking,
        }


class InvestmentType(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(50), nullable=False)
    definition = db.Column(db.Text, nullable=False)
    target = db.Column(db.Text, nullable=False)

    properties = db.relationship("Property", back_populates="investment_type")

    def to_dict(self):
        return {
            "id": self.id,
            "type": self.type,
            "definition": self.definition,
            "target": self.target,
        }
