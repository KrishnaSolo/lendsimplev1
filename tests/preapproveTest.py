import unittest
from unittest.mock import patch, MagicMock
from services.preapprove import pre_approve
from models.investor import Investor
from models.event import Event
from config import Config


class PreApproveTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.config = Config()
        cls.investor = Investor("John", "Doe", "johndoe@example.com")
        cls.event = Event("123 Main St", 100000, "Description", 1)

    @patch("services.preapprove.Flinks")
    @patch("models.investor.Investor.get_by_id")
    @patch("models.event.Event.get_by_id")
    def test_pre_approve_successful(
        self, mock_event_get, mock_investor_get, mock_flinks
    ):
        # Set up mocks
        mock_flinks.return_value = MagicMock(balance=200000)
        mock_investor_get.return_value = self.investor
        mock_event_get.return_value = self.event

        # Call the pre-approve service
        result = pre_approve(self.investor.id, self.event.id, 50000)

        # Assert that the result is true
        self.assertTrue(result)

    @patch("services.preapprove.Flinks")
    @patch("models.investor.Investor.get_by_id")
    @patch("models.event.Event.get_by_id")
    def test_pre_approve_insufficient_balance(
        self, mock_event_get, mock_investor_get, mock_flinks
    ):
        # Set up mocks
        mock_flinks.return_value = MagicMock(balance=10000)
        mock_investor_get.return_value = self.investor
        mock_event_get.return_value = self.event

        # Call the pre-approve service
        result = pre_approve(self.investor.id, self.event.id, 50000)

        # Assert that the result is false
        self.assertFalse(result)

    @patch("services.preapprove.Flinks")
    @patch("models.investor.Investor.get_by_id")
    @patch("models.event.Event.get_by_id")
    def test_pre_approve_exceeds_target(
        self, mock_event_get, mock_investor_get, mock_flinks
    ):
        # Set up mocks
        self.event.raised = 100000
        mock_flinks.return_value = MagicMock(balance=200000)
        mock_investor_get.return_value = self.investor
        mock_event_get.return_value = self.event

        # Call the pre-approve service
        result = pre_approve(self.investor.id, self.event.id, 50000)

        # Assert that the result is false
        self.assertFalse(result)
