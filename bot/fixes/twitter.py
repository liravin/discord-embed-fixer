import re

PATTERN = re.compile(r"^https?://(?:www\.)?(?:twitter|x)\.com/", re.IGNORECASE)


def fix(url: str) -> str:
    return re.sub(r"(?i)(https?://)(?:www\.)?(?:twitter|x)\.com", r"\1vxtwitter.com", url, count=1)
