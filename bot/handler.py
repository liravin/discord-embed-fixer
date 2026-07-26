import logging
from dataclasses import dataclass, field
from datetime import datetime


@dataclass(frozen=True)
class Message:
    author_id: int
    channel_id: int
    content: str
    timestamp: datetime
    attachment_urls: list[str] = field(default_factory=list)


async def handle_message(message: Message) -> None:
    logging.info(
        "[channel %s] %s: %s%s",
        message.channel_id,
        message.author_id,
        message.content,
        f" (attachments: {message.attachment_urls})" if message.attachment_urls else "",
    )

    content = message.content.strip()
