# Investor model code
from app import db


class Investor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(
        db.Integer, db.ForeignKey("user.id"), nullable=False, unique=True
    )
    bank_account_id = db.Column(
        db.Integer, db.ForeignKey("bank_account.id"), nullable=False
    )

    def __repr__(self):
        return f"<Investor {self.id}>"
