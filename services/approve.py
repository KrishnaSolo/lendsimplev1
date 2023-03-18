# Approve service code
import threading
import time
from ..main import app
from ..database import db
from ..models.event import InvestingEvent as Event
from ..models.investment import Investment
from ..models.notification import Notification
from ..services.book_of_records import BookOfRecords
from ..services.payments import PaymentService
from ..utils.logging import record_execution_time

approval_queue = []


@record_execution_time
def process_approval_queue():
    while True:
        if approval_queue:
            with app.app_context():
                event_id, investor_id, amount = approval_queue.pop(0)
                event = Event.query.filter_by(id=event_id).first()
                if not event:
                    app.logger.error(f"Event with id {event_id} not found")
                    Notification.create(
                        type="error", description=f"Event with id {event_id} not found"
                    )
                    continue
                with db.session.begin():
                    # Lock the event record for this transaction to ensure consistency
                    event = Event.query.filter_by(id=event_id).with_for_update().first()
                    if event.amount_raised + amount > event.target_amount:
                        app.logger.error(f"Target amount for event {event_id} exceeded")
                        Notification.create(
                            type="error",
                            description=f"Target amount for event {event_id} exceeded",
                            user_id=investor_id,
                        )
                        continue
                    investment = Investment(
                        event_id=event_id, investor_id=investor_id, amount=amount
                    )
                    db.session.add(investment)
                    db.session.flush()
                    try:
                        # Make the payment using Plooto
                        PaymentService.make_payment(
                            investor_id=investor_id,
                            holding_account_id=event.holding_account_id,
                            amount=amount,
                        )
                        # Record the transaction in the book of records
                        BookOfRecords.record_transaction(
                            investment_id=investment.id,
                            from_account_id=investor_id,
                            to_account_id=event.holding_account_id,
                            amount=amount,
                            description=f"Investment in event {event.id}",
                        )
                        # Update the amount raised for the event
                        event.amount_raised += amount
                        db.session.commit()
                        app.logger.info(
                            f"Investment of {amount} successfully processed for event {event_id}"
                        )
                        Notification.create(
                            type="success",
                            description=f"Investment of {amount} successfully processed for event {event_id}",
                            user_id=investor_id,
                        )
                    except Exception as e:
                        app.logger.error(
                            f"Error processing investment: {e}", exc_info=True
                        )
                        Notification.create(
                            type="error",
                            description=f"Error processing investment: {e}",
                            user_id=investor_id,
                        )
        else:
            time.sleep(1)


# Start the approval queue processing thread
t = threading.Thread(target=process_approval_queue)
t.start()


def add_to_approval_queue(event_id, investor_id, amount):
    approval_queue.append((event_id, investor_id, amount))
