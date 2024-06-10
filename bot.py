import os
import logging
import asyncio
from pyrogram import Client, filters
from pyrogram.handlers import MessageHandler
from aiohttp import web

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
        logger.info(f"Received /help command from chat {message.chat.id}")
        await client.send_message(message.chat.id, "How can I help you?")

    def run(self):
        logger.info("Starting HelpBot")
        self.bot.run()

# Health check server
async def health_check(request):
    return web.Response(text="OK")

def main():
    API_ID = int(os.environ.get("API_ID", ""))
    API_HASH = os.environ.get("API_HASH", "")
    BOT_TOKEN = os.environ.get("BOT_TOKEN", "")

    if not API_ID or not API_HASH or not BOT_TOKEN:
        logger.error("API_ID, API_HASH, or BOT_TOKEN environment variables are not set")
        exit(1)

    help_bot = HelpBot(API_ID, API_HASH, BOT_TOKEN)
    
    # Create a new event loop
    loop = asyncio.get_event_loop()

    # Set up the health check server
    app = web.Application()
    app.router.add_get('/health', health_check)
    runner = web.AppRunner(app)
    loop.run_until_complete(runner.setup())
    site = web.TCPSite(runner, '0.0.0.0', 8000)
    loop.run_until_complete(site.start())

    # Run the bot
    try:
        help_bot.run()
    except KeyboardInterrupt:
        logger.info("Bot stopped by user")
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
    finally:
        loop.run_until_complete(runner.cleanup())

if __name__ == "__main__":
    main()
