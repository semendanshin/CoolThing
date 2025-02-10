from datetime import datetime
from uuid import uuid4

from pydantic import BaseModel, Field, ConfigDict

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
