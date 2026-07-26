import re
from urllib.parse import urlsplit, urlunsplit, parse_qsl, urlencode

_URL_RE = re.compile(r"https?://\S+")
_TRAILING_PUNCTUATION = ").,]}\"'>"

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


def _fix_instagram(url: str) -> str | None:
    pattern = re.compile(r"^https?://(?:www\.)?instagram\.com/", re.IGNORECASE)
    if not pattern.match(url):
        return None
    return re.sub(r"(?i)(https?://)(?:www\.)?instagram\.com", r"\1oginstagram.com", url, count=1)


def _fix_youtube(url: str) -> str | None:
    pattern = re.compile(r"^https?://(?:www\.)?(?:youtube\.com/(?:watch|shorts/)|youtu\.be/)", re.IGNORECASE)
    if not pattern.match(url):
        return None
    parts = urlsplit(url)
    query = parse_qsl(parts.query, keep_blank_values=True)
    if parts.netloc.lower().endswith("youtube.com"):
        if parts.path.lower().startswith("/shorts/"):
            video_id = parts.path.rstrip("/").rsplit("/", 1)[-1]
        else:
            video_id = next((value for key, value in query if key == "v"), "")
    else:
        video_id = parts.path.strip("/")
    remaining_query = [(key, value) for key, value in query if key not in ("v", "si", "pp")]
    return urlunsplit(("https", "youtu.be", f"/{video_id}", urlencode(remaining_query), parts.fragment))


_FIXERS = (_fix_reddit, _fix_twitter, _fix_instagram, _fix_youtube)
