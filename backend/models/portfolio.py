# Portfolio model code
from backend.database import db


class Portfolio(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    investor_id = db.Column(db.Integer, db.ForeignKey("investor.id"), nullable=False)
    event_id = db.Column(db.Integer, db.ForeignKey("event.id"), nullable=False)
    amount = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return f"<Portfolio {self.id}>"

    def to_dict(self):
        return {
            "id": self.id,
            "investor_id": self.investor_id,
            "event_id": self.event_id,
            "amount": self.amount,
        }
