import uuid
from dataclasses import dataclass, field
from typing import Optional


@dataclass(kw_only=True)
class BundleCreateDTO:
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    name: str


@dataclass(kw_only=True)
class BundleUpdateDTO:
    name: Optional[str] = None

