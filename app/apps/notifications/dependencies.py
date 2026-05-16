from fastapi import Depends
from sqlalchemy.orm import Session

from core.database import get_db

from .repositories import NotificationRepository
from .services import NotificationService


def get_notification_repository(
    db: Session = Depends(get_db)
):
    return NotificationRepository(db)


def get_notification_service(
    repository: NotificationRepository = Depends(
        get_notification_repository
    )
):
    return NotificationService(repository)