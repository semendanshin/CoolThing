from dataclasses import dataclass
from typing import Optional


@dataclass(kw_only=True)
class WorkerCreateDTO:
    id: str
    app_id: str
    app_hash: str
    session_string: str
    proxy: str
    campaign_id: str
    role: str
    status: str


@dataclass(kw_only=True)
class WorkerUpdateDTO:
    id: str = None
    bio: Optional[str] = None
    username: Optional[str] = None
    app_id: Optional[str] = None
    app_hash: Optional[str] = None
    session_string: Optional[str] = None
    proxy: Optional[str] = None
    campaign_id: Optional[str] = None
    role: Optional[str] = None
    status: Optional[str] = None
