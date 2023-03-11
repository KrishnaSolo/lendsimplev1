import unittest
from app import create_app, db
from app.models import BankAccount, Event, Investment, Notification, User
from app.services.approve import approve_investors


class ApproveServiceTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app("testing")
        self.client = self.app.test_client()
        with self.app.app_context():
            db.create_all()

        # Create test user
        user = User(name="Test User", email="test@example.com", password="password")
        with self.app.app_context():
            db.session.add(user)
            db.session.commit()

        # Create test bank account
        bank_account = BankAccount(
            user_id=user.id,
            account_number="1234567890",
            institution_number="001",
            transit_number="12345",
        )
        with self.app.app_context():
            db.session.add(bank_account)
            db.session.commit()

        # Create test event
        event = Event(
            title="Test Event",
            description="A test event",
            target_amount=1000,
            active=True,
        )
        with self.app.app_context():
            db.session.add(event)
            db.session.commit()

        # Create test investment
        investment = Investment(amount=500, user_id=user.id, event_id=event.id)
        with self.app.app_context():
            db.session.add(investment)
            db.session.commit()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_approve_investors_success(self):
        with self.app.app_context():
            # Approve the investor
            approve_investors()

            # Check that the investment was processed
            investment = Investment.query.filter_by(user_id=1, event_id=1).first()
            self.assertIsNotNone(investment.processed_at)

            # Check that the event was locked
            event = Event.query.filter_by(id=1).first()
            self.assertTrue(event.locked)

            # Check that the transaction was recorded in the book of records
            self.assertEqual(len(event.book_of_records), 1)

            # Check that the amount raised was updated
            self.assertEqual(event.amount_raised, 500)

            # Check that a success notification was added
            notification = Notification.query.filter_by(
                user_id=1, type="success"
            ).first()
            self.assertIsNotNone(notification)

    def test_approve_investors_failure(self):
        with self.app.app_context():
            # Add an investment that would cause the target amount to be exceeded
            investment = Investment(amount=600, user_id=1, event_id=1)
            db.session.add(investment)
            db.session.commit()

            # Approve the investors
            approve_investors()

            # Check that the investment was not processed
            investment = Investment.query.filter_by(user_id=1, event_id=1).first()
            self.assertIsNone(investment.processed_at)

            # Check that the event was not locked
            event = Event.query.filter_by(id=1).first()
            self.assertFalse(event.locked)

            # Check that a failure notification was added
            notification = Notification.query.filter_by(
                user_id=1, type="failure"
            ).first()
            self.assertIsNotNone(notification)
