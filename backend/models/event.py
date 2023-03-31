# Event model code
from backend.database import db


class InvestingEvent(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    property_id = db.Column(db.Integer, db.ForeignKey("property.id"), nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    target_amount = db.Column(db.Float, nullable=False)
    amount_raised = db.Column(db.Float, default=0.0)
    active = db.Column(db.Boolean, default=True)

    def __repr__(self):
        return f"<InvestingEvent {self.id}>"

    def to_dict(self):
        return {
            "id": self.id,
            "property_id": self.property_id,
            "start_date": self.start_date.strftime("%Y-%m-%d %H:%M:%S"),
            "end_date": self.end_date.strftime("%Y-%m-%d %H:%M:%S"),
            "target_amount": self.target_amount,
            "amount_raised": self.amount_raised,
            "active": self.active,
        }
