from bot.client import bot
from bot.config import DISCORD_TOKEN
from bot.logging import setup_logging

if __name__ == "__main__":
    setup_logging()
    bot.run(DISCORD_TOKEN, log_handler=None)
