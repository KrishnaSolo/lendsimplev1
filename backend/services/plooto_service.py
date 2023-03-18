from plaid.errors import APIError, ItemError
from plaid import Client
from backend.models.investor import Investor
from backend.models.bank_account import BankAccount

from backend.utils.logging import record_execution_time
from backend.config import Config

import time
from retrying import retry

client = Client(
    client_id=Config.PLAID_CLIENT_ID,
    secret=Config.PLAID_SECRET,
    environment=Config.PLAID_ENV,
)


class PlootoService:
    @staticmethod
    @record_execution_time
    @retry(
        stop_max_attempt_number=4,
        wait_exponential_multiplier=1000,
        wait_exponential_max=60000,
    )
    def make_payment(investor_id, holding_account_id, amount):
        # Get investor's bank account info
        investor = Investor.query.get(investor_id)
        bank_account_id = investor.bank_account_id

        # Get holding account info
        holding_account = BankAccount.query.get(holding_account_id)
        bank_account_holder = holding_account.bank_account_holder
        bank_account_number = holding_account.bank_account_number
        bank_routing_number = holding_account.bank_routing_number

        # Send ACH payment through Plaid
        try:
            response = client.PaymentInitiation.create(
                {
                    "payment_idempotency_key": str(investor_id) + str(time.time()),
                    "payment": {
                        "value": amount,
                        "currency": "USD",
                        "ach": {
                            "account": bank_account_id,
                            "account_holder_name": bank_account_holder,
                            "account_number": bank_account_number,
                            "account_type": "checking",
                            "routing_number": bank_routing_number,
                        },
                    },
                }
            )

            return response.payment_id

        except (APIError, ItemError) as e:
            raise e
