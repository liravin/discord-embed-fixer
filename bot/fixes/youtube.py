import re
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit

PATTERN = re.compile(r"^https?://(?:www\.)?(?:youtube\.com|youtu\.be)/", re.IGNORECASE)


def fix(url: str) -> str:
    parts = urlsplit(url)
    query = [(key, value) for key, value in parse_qsl(parts.query, keep_blank_values=True) if key != "si"]
    return urlunsplit((parts.scheme, parts.netloc, parts.path, urlencode(query), parts.fragment))
