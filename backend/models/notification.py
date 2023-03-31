# Notification model code
from backend.database import db
from datetime import datetime


class Notification(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(50), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    description = db.Column(db.String(200), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return f"<Notification {self.id}>"

    def to_dict(self):
        return {
            "id": self.id,
            "type": self.type,
            "user_id": self.user_id,
            "description": self.description,
            "created_at": self.created_at.isoformat(),
        }
