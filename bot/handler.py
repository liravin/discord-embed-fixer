import logging
import re
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit

import discord
from discord.ext import commands

_URL_RE = re.compile(r"https?://\S+")
_TRAILING_PUNCTUATION = ").,]}\"'>"
_MAX_EMBEDS_PER_MESSAGE = 5


def _fix_reddit(url: str) -> str | None:
    pattern = re.compile(r"^https?://(?:www\.)?reddit\.com/", re.IGNORECASE)
    if not pattern.match(url):
        return None
    return re.sub(r"(?i)(https?://)(?:www\.)?reddit\.com", r"\1vxreddit.com", url, count=1)


def _fix_twitter(url: str) -> str | None:
    pattern = re.compile(r"^https?://(?:www\.)?(?:twitter|x)\.com/", re.IGNORECASE)
    if not pattern.match(url):
        return None
    return re.sub(r"(?i)(https?://)(?:www\.)?(?:twitter|x)\.com", r"\1vxtwitter.com", url, count=1)


def _fix_youtube(url: str) -> str | None:
    pattern = re.compile(r"^https?://(?:www\.)?(?:youtube\.com|youtu\.be)/", re.IGNORECASE)
    if not pattern.match(url):
        return None
    parts = urlsplit(url)
    query = [(key, value) for key, value in parse_qsl(parts.query, keep_blank_values=True) if key != "si"]
    return urlunsplit((parts.scheme, parts.netloc, parts.path, urlencode(query), parts.fragment))


_FIXERS = (_fix_reddit, _fix_twitter, _fix_youtube)


def _find_fixed_links(content: str) -> list[str]:
    fixed_links = []
    for match in _URL_RE.findall(content):
        url = match.rstrip(_TRAILING_PUNCTUATION)
        for fix in _FIXERS:
            fixed_url = fix(url)
            if fixed_url is not None:
                if fixed_url != url:
                    fixed_links.append(fixed_url)
                break
    return fixed_links


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


def register(bot: commands.Bot) -> None:
    @bot.event
    async def on_message(message: discord.Message) -> None:
        await handle_message(message)
