from typing import Optional

from backend.services.plooto_service import PlootoService

from backend.services.flinks_service import FlinksService
from backend.utils.logging import setup_logging
from backend.models.investor import Investor
from backend.models.event import InvestingEvent as Event

logger = setup_logging()


class PaymentService:
    @staticmethod
    def make_payment(investor: Investor, event: Event, amount: float) -> Optional[str]:
        """
        Makes a payment from the investor to the event holding account using Plooto and Flinks API.

        :param investor: Investor object.
        :param event: Event object.
        :param amount: Amount to be paid.

        :return: Transaction ID if payment is successful, else None.
        """

        # Call Flinks API to check investor's account balance
        balance = FlinksService.get_balance(investor.flinks_account_id)
        if balance < amount:
            logger.warning(
                f"Insufficient balance for investor {investor.id} in Flinks account."
            )
            return None

        # Make payment using Plooto API
        payment_id = PlootoService.make_payment(
            from_account=investor.plooto_account_id,
            to_account=event.holding_account_id,
            amount=amount,
        )

        return payment_id
