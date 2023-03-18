# Book_of_records model code
from ..database import db


class BookOfRecords(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    investor_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    property_id = db.Column(db.Integer, db.ForeignKey("property.id"), nullable=False)
    event_id = db.Column(
        db.Integer, db.ForeignKey("investing_event.id"), nullable=False
    )
    amount = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return f"<BookOfRecords {self.id}>"
