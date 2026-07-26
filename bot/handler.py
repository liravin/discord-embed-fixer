import logging

import discord
from discord.ext import commands

from bot.config import MAX_EMBEDS
from bot.fixing import _find_fixed_links

_MAX_EMBEDS_PER_MESSAGE = 5


async def handle_message(message: discord.Message) -> None:
    logging.info(
        "[channel %s] %s: %s%s",
        message.channel.id,
        message.author.id,
        message.clean_content,
        f" (attachments: {[a.url for a in message.attachments]})" if message.attachments else "",
    )

    fixed_links = _find_fixed_links(message.clean_content) # type: ignore
    if not fixed_links:
        return

    too_many = len(fixed_links) > MAX_EMBEDS
    for i in range(0, min(len(fixed_links), MAX_EMBEDS), _MAX_EMBEDS_PER_MESSAGE):
        batch = fixed_links[i : i + _MAX_EMBEDS_PER_MESSAGE]
        
        embed = "\n".join(batch)
        response = f"[Posted by {message.author.display_name}]({embed})"
        await message.channel.send(response)
    if too_many:
        await message.channel.send("Too many links to embed.")

    await message.delete()


def register(bot: commands.Bot) -> None:
    @bot.event
    async def on_message(message: discord.Message) -> None:
        await handle_message(message)
