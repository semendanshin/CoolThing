from dataclasses import dataclass

from domain.worker_settings import WorkerSettings, ManagerSettings, ParserSettings
from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.sql import text

from abstractions.repositories.bot_settings import BotSettingsRepositoryInterface


@dataclass
class SQLAlchemyBotSettingsRepository(BotSettingsRepositoryInterface):
    session_maker: async_sessionmaker

    _query = """
       SELECT
            w.id,
            w.app_id,
            w.app_hash,
            w.session_string,
            w.proxy,
            w.campaign_id,
            w.role,
            w.status,
            g.model,
            g.token,
            g.proxy AS openai_proxy,
            g.assistant,
            g.service_prompt,
            c.welcome_message,
            c.chats,
            c.plus_keywords,
            c.minus_keywords,
            c.new_lead_wait_interval_seconds,
            c.chat_answer_wait_interval_seconds
        FROM
            workers AS w
        JOIN
            campaigns AS c ON w.campaign_id = c.id
        JOIN
            gpt_settings AS g ON c.gpt_settings_id = g.id
        WHERE
            w.status = 'active' AND w.deleted_at IS NULL
    """

    async def get_active_bot_settings(self) -> list[WorkerSettings]:
        workers = []
        async with self.session_maker() as session:
            async with session.begin():
                result = await session.execute(text(self._query))
                for row in result:
                    base = WorkerSettings(
                        id=str(row.id),
                        app_id=row.app_id,
                        app_hash=row.app_hash,
                        session_string=row.session_string,
                        proxy=row.proxy,
                        campaign_id=str(row.campaign_id),
                        role=row.role,
                        status=row.status,
                    )
                    match row.role:
                        case "manager":
                            typing_and_sending_sleep_from, typing_and_sending_sleep_to = map(int, row.chat_answer_wait_interval_seconds.split("-"))
                            welcome_sleep_from, welcome_sleep_to = map(int, row.new_lead_wait_interval_seconds.split("-"))
                            worker = ManagerSettings(
                                **base.__dict__,
                                model=row.model,
                                token=row.token,
                                openai_proxy=row.openai_proxy,
                                assistant=row.assistant,
                                service_prompt=row.service_prompt,
                                welcome_message=row.welcome_message,
                                typing_and_sending_sleep_from=typing_and_sending_sleep_from,
                                typing_and_sending_sleep_to=typing_and_sending_sleep_to,
                                welcome_sleep_from=welcome_sleep_from,
                                welcome_sleep_to=welcome_sleep_to,
                            )
                        case "parser":
                            worker = ParserSettings(
                                **base.__dict__,
                                chats=row.chats,
                                plus_keywords=row.plus_keywords,
                                minus_keywords=row.minus_keywords,
                            )
                        case _:
                            worker = base

                    workers.append(worker)
        return workers
