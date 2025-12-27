import requests
from settings import Config # УБРАЛИ config.

class TelegramBot:
    def __init__(self):
        self.bot_token = Config.TELEGRAM_BOT_TOKEN
        self.channel_id = Config.TELEGRAM_CHANNEL_ID
