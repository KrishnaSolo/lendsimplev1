import unittest
import json
from app import create_app, db
from app.models.investor import Investor


class InvestorServiceTest(unittest.TestCase):
    def setUp(self):
        self.app = create_app(config_name="testing")
        self.client = self.app.test_client
        self.investor = {
            "name": "John Doe",
            "email": "johndoe@example.com",
            "password": "password",
        }

        with self.app.app_context():
            db.create_all()

    def register_investor(self, investor):
        return self.client().post(
            "/investors/", data=json.dumps(investor), content_type="application/json"
        )

    def test_investor_registration(self):
        res = self.register_investor(self.investor)
        self.assertEqual(res.status_code, 201)
        self.assertIn("id", str(res.data))

    def test_investor_duplicate_registration(self):
        self.register_investor(self.investor)
        res = self.register_investor(self.investor)
        self.assertEqual(res.status_code, 400)
        self.assertIn("Email already exists", str(res.data))

    def test_get_all_investors(self):
        self.register_investor(self.investor)
        res = self.client().get("/investors/")
        self.assertEqual(res.status_code, 200)
        self.assertIn("John Doe", str(res.data))

    def test_get_investor_by_id(self):
        self.register_investor(self.investor)
        investor = Investor.query.first()
        res = self.client().get(f"/investors/{investor.id}")
        self.assertEqual(res.status_code, 200)
        self.assertIn("John Doe", str(res.data))

    def test_update_investor(self):
        self.register_investor(self.investor)
        investor = Investor.query.first()
        updated_investor = {
            "name": "Jane Doe",
            "email": "janedoe@example.com",
            "password": "password",
        }
        res = self.client().put(
            f"/investors/{investor.id}",
            data=json.dumps(updated_investor),
            content_type="application/json",
        )
        self.assertEqual(res.status_code, 200)
        self.assertIn("Jane Doe", str(res.data))

    def test_delete_investor(self):
        self.register_investor(self.investor)
        investor = Investor.query.first()
        res = self.client().delete(f"/investors/{investor.id}")
        self.assertEqual(res.status_code, 204)

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()
