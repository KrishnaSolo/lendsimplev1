from ..models.book_of_records import BookOfRecords
from ..utils import log_metric, log_info


class BookOfRecordsService:
    @staticmethod
    def record_transaction(
        investment_id: int,
        from_account_id: str,
        to_account_id: str,
        amount: float,
        description: str,
    ) -> None:
        """
        Record a transaction in the book of records.

        Args:
            investment_id (int): The ID of the investment.
            from_account_id (str): The ID of the account from which the money is coming from.
            to_account_id (str): The ID of the account to which the money is going to.
            amount (float): The amount of money being transferred.
            description (str): The description of the transaction.
        """
        log_info(f"Recording transaction: {description}")
        BookOfRecords.record_transaction(
            investment_id=investment_id,
            from_account_id=from_account_id,
            to_account_id=to_account_id,
            amount=amount,
            description=description,
        )
        log_metric("transaction_recorded", amount)
