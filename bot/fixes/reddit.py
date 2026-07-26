import re

PATTERN = re.compile(r"^https?://(?:www\.)?reddit\.com/", re.IGNORECASE)


def fix(url: str) -> str:
    return re.sub(r"(?i)(https?://)(?:www\.)?reddit\.com", r"\1vxreddit.com", url, count=1)
