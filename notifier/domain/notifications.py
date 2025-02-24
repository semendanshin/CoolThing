from datetime import datetime
from typing import Optional, Annotated

from pydantic import BaseModel

from domain.events import Event


class Notification[user_pk_type](BaseModel):
    event: Event
    text: Optional[str] = None
    sent_at: Optional[datetime] = None
    send_to: Optional[user_pk_type] = None


class SendNotificationRequest(BaseModel):
    notification: Notification
    users: list[Annotated[int, 'Telegram user ID']]
