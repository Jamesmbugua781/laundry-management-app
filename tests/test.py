from app.core.database import SessionLocal

from app.apps.notifications.dependencies import get_notification_service


db = SessionLocal()

service = get_notification_service(db)

# TEST SMS (Africa's Talking)
service.send_sms(
    phone_number="+254115463607",
    message="Testing SMS from Laundry System 🚀"
)

# TEST EMAIL (Resend)
service.send_email(
    email="daxitjay21@gmail.com",
    subject="Test Email",
    body="Everything is working perfectly 🚀"
)

print("Tests executed")