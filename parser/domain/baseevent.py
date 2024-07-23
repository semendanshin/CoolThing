import uuid
from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class BaseEvent:
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    created_at: datetime = datetime.now()
