import discord
from discord.ext import commands

from bot.handler import Message, handle_message


def register(bot: commands.Bot) -> None:
    @bot.event
    async def on_message(message: discord.Message) -> None:
        if not isinstance(message.channel, discord.VoiceChannel):
            return

        await handle_message(
            Message(
                author_id=message.author.id,
                channel_id=message.channel.id,
                content=message.clean_content,
                timestamp=message.created_at,
                attachment_urls=[a.url for a in message.attachments],
            ),
        )
