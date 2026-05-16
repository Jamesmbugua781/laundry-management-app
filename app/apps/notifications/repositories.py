from sqlalchemy.orm import Session

from .models import Notification


class NotificationRepository:

    def __init__(self, db: Session):
        self.db = db

    def create_notification(
        self,
        recipient: str,
        message: str,
        type: str
    ):

        notification = Notification(
            recipient=recipient,
            message=message,
            type=type
        )

        self.db.add(notification)

        self.db.commit()

        self.db.refresh(notification)

        return notification