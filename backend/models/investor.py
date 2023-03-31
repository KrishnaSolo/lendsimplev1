# Investor model code
from backend.database import db
from backend.models.user import User
from backend.models.bank_account import BankAccount


class Investor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey(User.id), nullable=False, unique=True)
    bank_account_id = db.Column(
        db.Integer, db.ForeignKey(BankAccount.id), nullable=False
    )

    def __repr__(self):
        return f"<Investor {self.id}>"

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "bank_account_id": self.bank_account_id,
        }
