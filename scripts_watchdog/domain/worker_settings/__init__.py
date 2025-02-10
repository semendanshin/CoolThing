from datetime import datetime
from typing import Literal, Any
from uuid import uuid4

from pydantic import BaseModel, Field, ConfigDict
from pydantic.main import IncEx

from settings import ScriptsDBSettings, MQSettings, DBSettings, WatcherSettings, NotifierSettings


class ScriptToPerform(BaseModel):
    id: str
    script_for_campaign_id: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class WorkerSettings(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid4()))
    scripts_db: ScriptsDBSettings
    mq: MQSettings
    db: DBSettings
    watcher: WatcherSettings
    notifier: NotifierSettings
    script_to_perform: ScriptToPerform

    def model_dump(
        self,
        *,
        mode: Literal['json', 'python'] | str = 'python',
        include: IncEx = None,
        exclude: IncEx = None,
        context: Any | None = None,
        by_alias: bool = False,
        exclude_unset: bool = False,
        exclude_defaults: bool = False,
        exclude_none: bool = False,
        round_trip: bool = False,
        warnings: bool | Literal['none', 'warn', 'error'] = True,
        serialize_as_any: bool = False,
    ) -> dict[str, Any]:
        data = super().model_dump()
        print(data)
        data['scripts_db']['password'] = self.scripts_db.password.get_secret_value()
        data['db']['password'] = self.db.password.get_secret_value()
        return data



    def __hash__(self):
        return hash((
            self.id,
            self.scripts_db.name,
            self.scripts_db.host,
            self.scripts_db.port,
            self.db.user,
            self.db.host,
            self.db.port,
            self.watcher.base_url,
            self.mq.user,
            self.mq.host,
            self.mq.port,
            self.mq.vhost,
            self.notifier.base_url,
            self.script_to_perform.script_for_campaign_id,
            self.script_to_perform.id,
        ))
