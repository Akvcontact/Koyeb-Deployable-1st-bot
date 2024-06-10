import os
from pyrogram import Client, filters
from pyrogram.handlers import MessageHandler
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class HelpBot:
    def __init__(self, api_id, api_hash, bot_token):
        self.api_id = api_id
        self.api_hash = api_hash
        self.bot_token = bot_token
        self.bot = Client("help_bot", api_id=self.api_id, api_hash=self.api_hash, bot_token=self.bot_token)

        # Add handlers
        self.add_handlers()

    def add_handlers(self):
        self.bot.add_handler(MessageHandler(self.help_command, filters.command('help') & (filters.private | filters.group)))

    async def help_command(self, client, message):
        await client.send_message(message.chat.id, "How can I help you?")

    def run(self):
        self.bot.run()

# Instantiate and run the bot
if __name__ == "__main__":
    API_ID = int(os.environ.get("API_ID", "19341831"))
    API_HASH = os.environ.get("API_HASH", "d5dd7d867fc35ae9fa59c54e54d218ad")
    BOT_TOKEN = os.environ.get("BOT_TOKEN", "7167823797:AAHnrBgaWCWnSQ7F838QRAQO2auiboiJby0")

    help_bot = HelpBot(API_ID, API_HASH, BOT_TOKEN)
    help_bot.run()
