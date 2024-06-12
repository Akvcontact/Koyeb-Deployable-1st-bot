import os
import asyncio
from aiohttp import web
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Read environment variables
API_ID = os.getenv("API_ID", "19341831")
API_HASH = os.getenv("API_HASH", "d5dd7d867fc35ae9fa59c54e54d218ad")
BOT_TOKEN = os.getenv("BOT_TOKEN", "7167823797:AAHnrBgaWCWnSQ7F838QRAQO2auiboiJby0")
PORT = int(os.getenv("PORT", 8080))

# Validate API_ID
if API_ID and API_ID.isdigit():
    API_ID = int(API_ID)
else:
    logger.error("API_ID environment variable is not set or invalid")
    raise ValueError("API_ID environment variable is not set or invalid")

async def handle(request):
    return web.Response(text="Hello, World!")

async def main():
    app = web.Application()
    app.router.add_get('/', handle)
    
   runner = web.AppRunner(app)
    await runner.setup()

    # Using '0.0.0.0' to accept connections from any network interface
    site = web.TCPSite(runner, '0.0.0.0', PORT)
    logger.info(f"Starting server on port {PORT}")
    await site.start()


    # Keep the server running
    while True:
        await asyncio.sleep(3600)  # Sleep for 1 hour, effectively keeping the server running

if __name__ == "__main__":
    if not API_HASH or not BOT_TOKEN:
        logger.error("API_HASH or BOT_TOKEN environment variables are not set or invalid")
        raise ValueError("API_HASH or BOT_TOKEN environment variables are not set or invalid")
    
    try:
        asyncio.run(main())
    except Exception as e:
        logger.error(f"Application exited with error: {e}")
        raise
