import logging

from models import Script, Message

logger = logging.getLogger(__name__)


async def seed():
    script = Script(
        name="demo script",
        type="Native integration",
        bots_count=3,
        messages=[
            Message(bot_index=1, text="hi there how to buy drugs"),
            Message(bot_index=2, text="me and @3"),
            Message(bot_index=3, text="we're cops btw"),
        ]
    )
    await script.create()
    logger.info("Seeded successfully")
