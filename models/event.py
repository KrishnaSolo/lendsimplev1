# Event model code
from .. import db


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
