# Copyright (c) 2025 Nand Yaduwanshi <NoxxOP>
# Location: Supaul, Bihar
#
# All rights reserved.
#
# This code is the intellectual property of Nand Yaduwanshi.
# You are not allowed to copy, modify, redistribute, or use this
# code for commercial or personal projects without explicit permission.

import asyncio
import importlib
from pyrogram import idle
from pyrogram.types import BotCommand
from pytgcalls.exceptions import NoActiveGroupCall
import config
from ShrutiMusic import LOGGER, app, userbot
from ShrutiMusic.core.call import Nand
from ShrutiMusic.misc import sudo
from ShrutiMusic.plugins import ALL_MODULES
from ShrutiMusic.utils.database import get_banned_users, get_gbanned
from config import BANNED_USERS

# Bot Commands List
COMMANDS = [
    BotCommand("start", "🚀 Start bot"),
    BotCommand("help", "❓ Help menu and Many More Management Commands"),
    BotCommand("ping", "📡 Ping and system stats"),
    BotCommand("play", "🎵 Start streaming the requested track"),
    BotCommand("vplay", "📹 Start video streaming"),
    BotCommand("playrtmps", "📺 Play Live Video"),
    BotCommand("playforce", "⚠️ Force play audio track"),
    BotCommand("vplayforce", "⚠️ Force play video track"),
    BotCommand("pause", "⏸ Pause the stream"),
    BotCommand("resume", "▶️ Resume the stream"),
    BotCommand("skip", "⏭ Skip the current track"),
    BotCommand("end", "🛑 End the stream"),
    BotCommand("stop", "🛑 Stop the stream"),
    BotCommand("queue", "📄 Show track queue"),
    BotCommand("auth", "➕ Add a user to auth list"),
    BotCommand("unauth", "➖ Remove a user from auth list"),
    BotCommand("authusers", "👥 Show list of auth users"),
    BotCommand("cplay", "📻 Channel audio play"),
    BotCommand("cvplay", "📺 Channel video play"),
    BotCommand("cplayforce", "🚨 Channel force audio play"),
    BotCommand("cvplayforce", "🚨 Channel force video play"),
    BotCommand("channelplay", "🔗 Connect group to channel"),
    BotCommand("loop", "🔁 Enable/disable loop"),
    BotCommand("stats", "📊 Bot stats"),
    BotCommand("shuffle", "🔀 Shuffle the queue"),
    BotCommand("seek", "⏩ Seek forward"),
    BotCommand("seekback", "⏪ Seek backward"),
    BotCommand("song", "🎶 Download song (mp3/mp4)"),
    BotCommand("speed", "⏩ Adjust audio playback speed (group)"),
    BotCommand("cspeed", "⏩ Adjust audio speed (channel)"),
    BotCommand("tagall", "📢 Tag everyone"),
]

async def setup_bot_commands():
    """Setup bot commands during startup"""
    try:
        await app.set_bot_commands(COMMANDS)
        LOGGER("ShrutiMusic").info("Bot commands set successfully!")
    except Exception as e:
        LOGGER("ShrutiMusic").error(f"Failed to set bot commands: {str(e)}")

async def init():
    # Ensure at least one assistant is configured
    if not any([config.STRING1, config.STRING2, config.STRING3, config.STRING4, config.STRING5]):
        LOGGER(__name__).error("Assistant client variables not defined, exiting...")
        return

    await sudo()

    # Load banned users
    try:
        users = await get_gbanned()
        for user_id in users:
            BANNED_USERS.add(user_id)
        users = await get_banned_users()
        for user_id in users:
            BANNED_USERS.add(user_id)
    except Exception:
        pass

    await app.start()
    await setup_bot_commands()

    # Import all modules/plugins
    for all_module in ALL_MODULES:
        importlib.import_module("ShrutiMusic.plugins." + all_module)

    LOGGER("ShrutiMusic.plugins").info("Successfully Imported Modules...")

    # Start userbot assistants
    await userbot.start()

    # Start PyTgCalls
    await Nand.start()
    try:
        await Nand.stream_call("https://te.legra.ph/file/29f784eb49d230ab62e9e.mp4")
    except NoActiveGroupCall:
        LOGGER("ShrutiMusic").error(
            "Please turn on the videochat of your log group/channel.\nStopping Bot..."
        )
        return
    except Exception:
        pass

    await Nand.decorators()

    LOGGER("ShrutiMusic").info(
        "Shruti Music Started Successfully.\n\nDo not forget to visit @ShrutiBots"
    )

    await idle()

    # Stop everything safely
    await app.stop()
    await userbot.stop()
    LOGGER("ShrutiMusic").info("Stopping Shruti Music Bot...🥺")

if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(init())
