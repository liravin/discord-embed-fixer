import asyncio
import logging
import signal

import discord
from discord.ext import commands

from bot import handler

intents = discord.Intents.default()
intents.voice_states = True
intents.guilds = True
intents.message_content = True

bot = commands.Bot(command_prefix="!kt", intents=intents)


async def _setup_hook() -> None:
    # loop.add_signal_handler isn't supported on Windows event loops, so this
    # is a no-op there. It matters on Unix deployments (e.g. `docker stop`,
    # systemd), where SIGTERM would otherwise kill the process without
    # Client.close() running, skipping the voice-client disconnects.
    loop = asyncio.get_running_loop()
    try:
        loop.add_signal_handler(signal.SIGTERM, lambda: asyncio.create_task(bot.close()))
    except NotImplementedError:
        logging.debug("SIGTERM handler not supported on this platform, skipping")


bot.setup_hook = _setup_hook


@bot.event
async def on_ready():
    logging.info("Logged in as %s (%s)", bot.user, bot.user.id)


handler.register(bot)
