import logging
import re

import discord

from bot.fixes import reddit, twitter, youtube

_URL_RE = re.compile(r"https?://\S+")
_TRAILING_PUNCTUATION = ").,]}\"'>"
_FIXERS = (reddit, twitter, youtube)
_MAX_EMBEDS_PER_MESSAGE = 5


async def handle_message(message: discord.Message) -> None:
    logging.info(
        "[channel %s] %s: %s%s",
        message.channel.id,
        message.author.id,
        message.clean_content,
        f" (attachments: {[a.url for a in message.attachments]})" if message.attachments else "",
    )

    fixed_links = _find_fixed_links(message.clean_content)
    if not fixed_links:
        return

    await message.edit(suppress=True)

    for i in range(0, len(fixed_links), _MAX_EMBEDS_PER_MESSAGE):
        batch = fixed_links[i : i + _MAX_EMBEDS_PER_MESSAGE]
        await message.channel.send("\n".join(batch))


def _find_fixed_links(content: str) -> list[str]:
    fixed_links = []
    for match in _URL_RE.findall(content):
        url = match.rstrip(_TRAILING_PUNCTUATION)
        for fixer in _FIXERS:
            if fixer.PATTERN.match(url):
                fixed_url = fixer.fix(url)
                if fixed_url != url:
                    fixed_links.append(fixed_url)
                break
    return fixed_links
