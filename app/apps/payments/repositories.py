 from sqlalchemy.orm import Session

from .models import Payment


class PaymentRepository:

    def __init__(self, db: Session):
        self.db = db

    def create_payment(
        self,
        order_id: int,
        phone_number: str,
        amount: int,
        checkout_request_id: str,
        merchant_request_id: str
    ):

        payment = Payment(
            order_id=order_id,
            phone_number=phone_number,
            amount=amount,
            checkout_request_id=checkout_request_id,
            merchant_request_id=merchant_request_id,
            status="PENDING"
        )

        self.db.add(payment)

        self.db.commit()

        self.db.refresh(payment)

        return payment

    def get_by_checkout_request_id(
        self,
        checkout_request_id: str
    ):

        return self.db.query(Payment).filter(
            Payment.checkout_request_id ==
            checkout_request_id
        ).first()

    def mark_as_success(
        self,
        checkout_request_id: str,
        mpesa_receipt: str
    ):

        payment = self.get_by_checkout_request_id(
            checkout_request_id
        )

        if not payment:
            return None

        payment.status = "SUCCESS"

        payment.mpesa_receipt = mpesa_receipt

        self.db.commit()

        self.db.refresh(payment)

        return payment

    def mark_as_failed(
        self,
        checkout_request_id: str
    ):

        payment = self.get_by_checkout_request_id(
            checkout_request_id
        )

        if not payment:
            return None

        payment.status = "FAILED"

        self.db.commit()

        self.db.refresh(payment)

        return payment