from ..models.investor import Investor
import plooto
import os

from ..utils import record_execution_time, increment_counter


class PlootoService:
    """
    A service for interacting with Plooto API for making payments to investors
    """

    @staticmethod
    @record_execution_time("plooto-payment", "info")
    @increment_counter("plooto-payment-counter")
    def make_payment(investor_id: str, holding_account_id: str, amount: float) -> bool:
        """
        Makes a payment to an investor using Plooto API.
        :param investor_id: The ID of the investor to pay.
        :param holding_account_id: The ID of the holding account to transfer funds from.
        :param amount: The amount to pay to the investor.
        :return: True if payment was successful, False otherwise.
        """
        # Get Plooto credentials from environment variables
        api_key = os.getenv("PLOOTO_API_KEY")
        api_secret = os.getenv("PLOOTO_API_SECRET")
        access_token = os.getenv("PLOOTO_ACCESS_TOKEN")

        # Create Plooto client
        client = plooto.Client(api_key, api_secret, access_token)

        # Retrieve investor's bank account information
        investor = Investor.query.filter_by(id=investor_id).first()
        bank_account_id = investor.bank_account_id

        # Create Plooto payment
        payment = client.create_payment(
            amount=amount,
            from_account_id=holding_account_id,
            to_bank_account_id=bank_account_id,
            message=f"Payment to investor {investor_id}",
        )

        # Process payment
        response = payment.process()

        # Check if payment was successful
        if response["status"] == "success":
            return True

        return False
