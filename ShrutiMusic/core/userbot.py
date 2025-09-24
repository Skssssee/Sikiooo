# Copyright (c) 2025 Nand Yaduwanshi <NoxxOP>
# Location: Supaul, Bihar
#
# This file has been sanitized to remove insecure/obfuscated behavior.
# Removed: secret/config exfiltration, auto-join to unknown chats, obfuscated constants.

import asyncio
import logging
from pyrogram import Client
import config  # your project config (API_ID, API_HASH, STRING1..STRING5, BOT_TOKEN, etc.)

# Use standard logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

assistants = []     # list of assistant indices that were started (1..5)
assistant_ids = []  # actual numeric user ids for started assistants


class Userbot:
    """
    Manage up to 5 assistant Pyrogram Clients.
    Each assistant uses a separate string session in config: STRING1..STRING5
    """

    def __init__(self):
        # create Client instances for each possible assistant
        # Note: `no_updates=True` avoids pulling updates (useful for helper assistants)
        self.one = Client(
            name="Assistant1",
            api_id=config.API_ID,
            api_hash=config.API_HASH,
            session_string=getattr(config, "STRING1", None),
            no_updates=True,
        )
        self.two = Client(
            name="Assistant2",
            api_id=config.API_ID,
            api_hash=config.API_HASH,
            session_string=getattr(config, "STRING2", None),
            no_updates=True,
        )
        self.three = Client(
            name="Assistant3",
            api_id=config.API_ID,
            api_hash=config.API_HASH,
            session_string=getattr(config, "STRING3", None),
            no_updates=True,
        )
        self.four = Client(
            name="Assistant4",
            api_id=config.API_ID,
            api_hash=config.API_HASH,
            session_string=getattr(config, "STRING4", None),
            no_updates=True,
        )
        self.five = Client(
            name="Assistant5",
            api_id=config.API_ID,
            api_hash=config.API_HASH,
            session_string=getattr(config, "STRING5", None),
            no_updates=True,
        )

    async def get_bot_username_from_token(self, token: str) -> str | None:
        """
        Safely obtain bot username from a bot token.
        This starts a temporary client (no persistent session created).
        """
        if not token:
            return None
        try:
            temp = Client(
                name="temp_bot_client",
                api_id=config.API_ID,
                api_hash=config.API_HASH,
                bot_token=token,
                no_updates=True,
            )
            await temp.start()
            username = getattr(temp.me, "username", None)
            await temp.stop()
            return username
        except Exception as exc:
            logger.exception("Failed to fetch bot username: %s", exc)
            return None

    async def start_assistants(self):
        """
        Start configured assistant accounts. Each assistant will be started only
        if the matching STRINGx exists in config.
        No config or secrets are sent anywhere.
        """
        logger.info("Starting assistants (if configured)...")

        # Helper to start a client and log minimal info
        async def _start_and_register(client_obj, idx):
            try:
                if client_obj.session_name is None and client_obj.session_string is None:
                    # nothing configured for this assistant
                    return False
                await client_obj.start()
                uid = client_obj.me.id
                uname = getattr(client_obj.me, "username", None)
                assistants.append(idx)
                assistant_ids.append(uid)
                logger.info("Assistant %d started: id=%s username=%s", idx, uid, uname)
                return True
            except Exception as exc:
                logger.exception("Assistant %d failed to start: %s", idx, exc)
                return False

        # Start each configured assistant
        if getattr(config, "STRING1", None):
            await _start_and_register(self.one, 1)
        if getattr(config, "STRING2", None):
            await _start_and_register(self.two, 2)
        if getattr(config, "STRING3", None):
            await _start_and_register(self.three, 3)
        if getattr(config, "STRING4", None):
            await _start_and_register(self.four, 4)
        if getattr(config, "STRING5", None):
            await _start_and_register(self.five, 5)

        logger.info("Assistants started: %s", assistants)

    async def stop_assistants(self):
        """
        Stop any started assistants. Safe teardown.
        """
        logger.info("Stopping assistants...")
        try:
            if 1 in assistants:
                await self.one.stop()
                logger.info("Assistant 1 stopped.")
            if 2 in assistants:
                await self.two.stop()
                logger.info("Assistant 2 stopped.")
            if 3 in assistants:
                await self.three.stop()
                logger.info("Assistant 3 stopped.")
            if 4 in assistants:
                await self.four.stop()
                logger.info("Assistant 4 stopped.")
            if 5 in assistants:
                await self.five.stop()
                logger.info("Assistant 5 stopped.")
        except Exception as exc:
            logger.exception("Error stopping assistants: %s", exc)

    # 🔹 NEW ALIASES (to fix AttributeError in __main__.py)
    async def start(self):
        """Alias for start_assistants(), so you can call `await userbot.start()`"""
        return await self.start_assistants()

    async def stop(self):
        """Alias for stop_assistants(), so you can call `await userbot.stop()`"""
        return await self.stop_assistants()


# Example usage (safe)
async def main():
    ub = Userbot()
    await ub.start()

    # Safe info logging only (do NOT print secrets)
    bot_uname = await ub.get_bot_username_from_token(getattr(config, "BOT_TOKEN", None))
    logger.info("Managed bot username: %s", bot_uname)

    # keep running or perform helper tasks
    # await asyncio.sleep(...) or integrate with your main program

    # when shutting down:
    # await ub.stop()


if __name__ == "__main__":
    asyncio.run(main())
