import asyncio

from telethon import TelegramClient as Client
from telethon.tl.functions.channels import JoinChannelRequest
from telethon.sessions import StringSession
from telethon.tl.functions.messages import ImportChatInviteRequest


async def main():
    client = Client(
        session=StringSession(
            "1ApWapzMBu2Yy_AdmgfsTwAH1sOn-_bjhBIHKUCenH7pLe0pkuvjUPOOJAqNbllQY5O0JSiWuUiY9-ne3Hq9X6iMpDmFDA5UD-3BVdBkd0Yq2tkgGEXr1C4HCCa2c21UO_SwUt4bN1amJxGwiJ1YFF0__8Zb9IrJQn5WlHRhlzuZ2roL-XfbBHCYZS5WN1QPRG42g4DxckT0R3q2ZMX2f8k8dHN6CjuEfuM9gAacRNS48BBMqKsuFh1s-BhIiPV8NirIaDxsLMmqAqwjk5onEJ4uie2OjBqoByZ3Mf5YMlyRrx-8IYuD69gD-Zkf4KqgjPXCZFWXLbuT26uy2fyuWQAj2IDovl0w="),
        api_id=24278908,
        api_hash="24dce518fdb91ae7397d84f7a2e07a97",

    )
    chat = "https://t.me/testmeowtest"

    await client.connect()

    entity = await client.get_entity(chat)

    await client(JoinChannelRequest(entity))

    await client.disconnect()


asyncio.run(main())