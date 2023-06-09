# Investment model code
from backend.database import db


class Investment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    investor_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    event_id = db.Column(
        db.Integer, db.ForeignKey("investing_event.id"), nullable=False
    )
    amount_invested = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return f"<Investment {self.id}>"

    def to_dict(self):
        return {
            "id": self.id,
            "investor_id": self.investor_id,
            "event_id": self.event_id,
            "amount_invested": self.amount_invested,
        }
