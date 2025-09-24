from pyrogram import Client
import asyncio
import config
from ..logging import LOGGER

assistants = []
assistantids = []

class Userbot(Client):
    def __init__(self):
        self.one = Client(
            name="NandAss1",
            api_id=config.API_ID,
            api_hash=config.API_HASH,
            session_string=str(config.STRING1),
            no_updates=True,
        )
        self.two = Client(
            name="NandAss2",
            api_id=config.API_ID,
            api_hash=config.API_HASH,
            session_string=str(config.STRING2),
            no_updates=True,
        )
        self.three = Client(
            name="NandAss3",
            api_id=config.API_ID,
            api_hash=config.API_HASH,
            session_string=str(config.STRING3),
            no_updates=True,
        )
        self.four = Client(
            name="NandAss4",
            api_id=config.API_ID,
            api_hash=config.API_HASH,
            session_string=str(config.STRING4),
            no_updates=True,
        )
        self.five = Client(
            name="NandAss5",
            api_id=config.API_ID,
            api_hash=config.API_HASH,
            session_string=str(config.STRING5),
            no_updates=True,
        )

    async def join_all_support_centers(self, client):
        # Optional: remove or implement if assistants need to join groups
        pass

    async def start(self) -> None:
        LOGGER(__name__).info("Starting Assistants...")

        for idx, client, session in [
            (1, self.one, config.STRING1),
            (2, self.two, config.STRING2),
            (3, self.three, config.STRING3),
            (4, self.four, config.STRING4),
            (5, self.five, config.STRING5),
        ]:
            if session:
                await client.start()
                assistants.append(idx)
                assistant_id = client.me.id
                assistant_username = getattr(client.me, "username", "NoUsername")
                assistant_mention = client.me.mention
                assistantids.append(assistant_id)

                LOGGER(__name__).info(f"Assistant {idx} Started as {assistant_mention}")

                try:
                    await client.send_message(config.LOG_GROUP_ID, f"Assistant {idx} Started")
                except Exception:
                    LOGGER(__name__).error(
                        f"Assistant {idx} cannot access the log group. Add it and promote as admin!"
                    )
                    raise RuntimeError(f"Assistant {idx} cannot access log group")

    async def stop(self) -> None:
        LOGGER(__name__).info("Stopping Assistants...")
        for client, session in [
            (self.one, config.STRING1),
            (self.two, config.STRING2),
            (self.three, config.STRING3),
            (self.four, config.STRING4),
            (self.five, config.STRING5),
        ]:
            if session:
                await client.stop()
