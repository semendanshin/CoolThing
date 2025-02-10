from dataclasses import dataclass

from domain.events import BaseEvent


@dataclass(kw_only=True)
class NewActiveScript(BaseEvent):
    script_for_campaign_id: str
