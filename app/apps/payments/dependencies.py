 from fastapi import Depends
from sqlalchemy.orm import Session

from core.database import get_db

from .repositories import PaymentRepository
from .services import PaymentService

from features.notifications.dependencies import (
    get_notification_service
)


def get_payment_repository(
    db: Session = Depends(get_db)
):

    return PaymentRepository(db)


def get_payment_service(

    repository: PaymentRepository = Depends(
        get_payment_repository
    ),

    notification_service = Depends(
        get_notification_service
    )
):

    return PaymentService(
        repository,
        notification_service
    )