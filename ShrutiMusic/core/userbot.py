import asyncio
import logging
from pyrogram import Client
import config  # your project config (API_ID, API_HASH, STRING1..STRING5, BOT_TOKEN, etc.)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

assistants = []     # indices of started assistants (1..5)
assistant_ids = []  # numeric user IDs of started assistants


class Userbot:
    """
    Manage up to 5 assistant Pyrogram Clients.
    Each assistant uses a separate string session in config: STRING1..STRING5
    """

    def __init__(self):
        # create clients with optional session strings
        self.clients = []
        for i in range(1, 6):
            session_str = getattr(config, f"STRING{i}", None)
            client = Client(
                name=f"Assistant{i}",
                api_id=config.API_ID,
                api_hash=config.API_HASH,
                session_string=session_str,
                no_updates=True,
            )
            self.clients.append(client)

    async def get_bot_username_from_token(self, token: str | None) -> str | None:
        """Safely get bot username using a temporary client."""
        if not token:
            return None
        try:
            async with Client(
                name="temp_bot_client",
                api_id=config.API_ID,
                api_hash=config.API_HASH,
                bot_token=token,
                no_updates=True,
            ) as temp:
                return getattr(temp.me, "username", None)
        except Exception as exc:
            logger.exception("Failed to fetch bot username: %s", exc)
            return None

    async def start_assistants(self):
        """Start all configured assistants."""
        logger.info("Starting assistants (if configured)...")

        for idx, client in enumerate(self.clients, start=1):
            session_str = getattr(config, f"STRING{idx}", None)
            if not session_str:
                continue  # skip if no session string configured
            try:
                await client.start()
                uid = client.me.id
                uname = getattr(client.me, "username", None)
                assistants.append(idx)
                assistant_ids.append(uid)
                logger.info("Assistant %d started: id=%s username=%s", idx, uid, uname)
            except Exception as exc:
                logger.exception("Assistant %d failed to start: %s", idx, exc)

        logger.info("Assistants started: %s", assistants)

    async def stop_assistants(self):
        """Stop any started assistants safely."""
        logger.info("Stopping assistants...")
        for idx, client in enumerate(self.clients, start=1):
            if idx in assistants:
                try:
                    await client.stop()
                    logger.info("Assistant %d stopped.", idx)
                except Exception as exc:
                    logger.exception("Error stopping assistant %d: %s", idx, exc)

    # 🔹 aliases for convenience
    async def start(self):
        return await self.start_assistants()

    async def stop(self):
        return await self.stop_assistants()


# Example usage
async def main():
    ub = Userbot()
    await ub.start()

    bot_uname = await ub.get_bot_username_from_token(getattr(config, "BOT_TOKEN", None))
    logger.info("Managed bot username: %s", bot_uname)

    # Keep running or integrate with your main program
    # await asyncio.sleep(...)

    # On shutdown
    # await ub.stop()


if __name__ == "__main__":
    asyncio.run(main())