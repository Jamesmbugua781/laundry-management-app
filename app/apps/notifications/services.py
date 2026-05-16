import africastalking
import resend

from core.config import settings

from .repositories import (
    NotificationRepository
)


class NotificationService:

    def __init__(
        self,
        repository: NotificationRepository
    ):

        self.repository = repository

        # AFRICAS TALKING
        africastalking.initialize(
            username=settings.AT_USERNAME,
            api_key=settings.AT_API_KEY
        )

        self.sms = africastalking.SMS

        # RESEND
        resend.api_key = (
            settings.RESEND_API_KEY
        )

    # -----------------------------------
    # SEND SMS
    # -----------------------------------

    def send_sms(
        self,
        phone_number: str,
        message: str
    ):

        response = self.sms.send(
            message,
            [phone_number]
        )

        self.repository.create_notification(
            recipient=phone_number,
            message=message,
            type="SMS"
        )

        return response

    # -----------------------------------
    # SEND EMAIL
    # -----------------------------------

    def send_email(
        self,
        email: str,
        subject: str,
        body: str
    ):

        params = {
            "from": settings.FROM_EMAIL,
            "to": [email],
            "subject": subject,
            "html": f"<p>{body}</p>"
        }

        response = resend.Emails.send(
            params
        )

        self.repository.create_notification(
            recipient=email,
            message=body,
            type="EMAIL"
        )

        return response