from abc import ABC
from dataclasses import dataclass, field
from uuid import uuid4, UUID


@dataclass
class Model(ABC):
    id: UUID = field(default_factory=uuid4)
