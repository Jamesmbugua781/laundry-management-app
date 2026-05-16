 import base64
from datetime import datetime

import requests

from core.settings import settings

from .repositories import PaymentRepository

from features.notifications.services import (
    NotificationService
)


class PaymentService:

    def __init__(
        self,
        repository: PaymentRepository,
        notification_service: NotificationService
    ):

        self.repository = repository

        self.notification_service = (
            notification_service
        )

    # -----------------------------------
    # GENERATE ACCESS TOKEN
    # -----------------------------------

    def generate_access_token(self):

        url = (
            "https://sandbox.safaricom.co.ke/"
            "oauth/v1/generate"
            "?grant_type=client_credentials"
        )

        response = requests.get(
            url,
            auth=(
                settings.CONSUMER_KEY,
                settings.CONSUMER_SECRET
            )
        )

        data = response.json()

        return data["access_token"]

    # -----------------------------------
    # GENERATE PASSWORD
    # -----------------------------------

    def generate_password(self):

        timestamp = datetime.now().strftime(
            "%Y%m%d%H%M%S"
        )

        data_to_encode = (
            str(settings.BUSINESS_SHORTCODE)
            + settings.PASSKEY
            + timestamp
        )

        password = base64.b64encode(
            data_to_encode.encode()
        ).decode()

        return password, timestamp

    # -----------------------------------
    # INITIATE STK PUSH
    # -----------------------------------

    def initiate_stk_push(
        self,
        order_id: int,
        phone_number: str,
        amount: int
    ):

        access_token = (
            self.generate_access_token()
        )

        password, timestamp = (
            self.generate_password()
        )

        url = (
            "https://sandbox.safaricom.co.ke/"
            "mpesa/stkpush/v1/processrequest"
        )

        headers = {
            "Authorization":
            f"Bearer {access_token}"
        }

        payload = {
            "BusinessShortCode":
            settings.BUSINESS_SHORTCODE,

            "Password":
            password,

            "Timestamp":
            timestamp,

            "TransactionType":
            "CustomerPayBillOnline",

            "Amount":
            amount,

            "PartyA":
            phone_number,

            "PartyB":
            settings.BUSINESS_SHORTCODE,

            "PhoneNumber":
            phone_number,

            "CallBackURL":
            settings.CALLBACK_URL,

            "AccountReference":
            "Laundry",

            "TransactionDesc":
            "Laundry Payment"
        }

        response = requests.post(
            url,
            json=payload,
            headers=headers
        )

        data = response.json()

        payment = (
            self.repository.create_payment(
                order_id=order_id,
                phone_number=phone_number,
                amount=amount,
                checkout_request_id=data[
                    "CheckoutRequestID"
                ],
                merchant_request_id=data[
                    "MerchantRequestID"
                ]
            )
        )

        return payment

    # -----------------------------------
    # PROCESS CALLBACK
    # -----------------------------------

    def process_callback(
        self,
        callback_data: dict
    ):

        stk_callback = (
            callback_data["Body"]
            ["stkCallback"]
        )

        checkout_request_id = (
            stk_callback["CheckoutRequestID"]
        )

        result_code = (
            stk_callback["ResultCode"]
        )

        # PAYMENT FAILED
        if result_code != 0:

            return self.repository.mark_as_failed(
                checkout_request_id
            )

        callback_metadata = (
            stk_callback["CallbackMetadata"]
            ["Item"]
        )

        mpesa_receipt = None

        for item in callback_metadata:

            if item["Name"] == (
                "MpesaReceiptNumber"
            ):

                mpesa_receipt = item["Value"]

        payment = (
            self.repository.mark_as_success(
                checkout_request_id,
                mpesa_receipt
            )
        )

        # SEND SMS
        self.notification_service.send_sms(
            payment.phone_number,
            (
                f"Payment of KES "
                f"{payment.amount} "
                f"received successfully. "
                f"Receipt: "
                f"{payment.mpesa_receipt}"
            )
        )

        return payment