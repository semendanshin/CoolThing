from datetime import datetime

from pydantic import BaseModel


class Model(BaseModel):
    id: str
    created_at: datetime
    updated_at: datetime
