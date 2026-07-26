import os

from dotenv import load_dotenv

load_dotenv()

DISCORD_TOKEN = os.environ["DISCORD_TOKEN"]
MAX_EMBEDS = int(os.environ.get("MAX_EMBEDS", "10"))
