from app.models.notification import Notification
from app.database import SessionLocal


def add_notification(message: str):
    """Adds a new notification to the database."""
    db = SessionLocal()
    notif = Notification(message=message)
    db.add(notif)
    db.commit()
    db.close()
