# Investor model code
from ..database import db
from .user import User
from .bank_account import BankAccount


class Investor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey(User.id), nullable=False, unique=True)
    bank_account_id = db.Column(
        db.Integer, db.ForeignKey(BankAccount.id), nullable=False
    )

    def __repr__(self):
        return f"<Investor {self.id}>"
