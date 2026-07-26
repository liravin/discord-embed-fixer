import discord
from discord.ext import commands

from bot.handler import handle_message


def register(bot: commands.Bot) -> None:
    @bot.event
    async def on_message(message: discord.Message) -> None:
        await handle_message(message)
