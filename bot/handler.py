import logging

import discord
from discord.ext import commands

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

    await message.edit(suppress=True)

    for i in range(0, len(fixed_links), _MAX_EMBEDS_PER_MESSAGE):
        batch = fixed_links[i : i + _MAX_EMBEDS_PER_MESSAGE]
        await message.channel.send("\n".join(batch))


def register(bot: commands.Bot) -> None:
    @bot.event
    async def on_message(message: discord.Message) -> None:
        await handle_message(message)
