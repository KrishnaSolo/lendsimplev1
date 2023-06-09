# Bank_account model code
from backend.database import db


class BankAccount(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    account_number = db.Column(db.String(50), nullable=False)
    institution_number = db.Column(db.String(50), nullable=False)
    transit_number = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return f"<BankAccount {self.id}>"

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "account_number": self.account_number,
            "institution_number": self.institution_number,
            "transit_number": self.transit_number,
        }
