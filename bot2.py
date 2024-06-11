import os
import asyncio
from aiohttp import web

# Read environment variables as strings
API_ID = os.getenv("API_ID","19341831")
API_HASH = os.getenv("API_HASH","d5dd7d867fc35ae9fa59c54e54d218ad")
BOT_TOKEN = os.getenv("BOT_TOKEN","7167823797:AAHnrBgaWCWnSQ7F838QRAQO2auiboiJby0")

# Ensure that API_ID is treated as a string and check its validity
if API_ID and API_ID.isdigit():
    API_ID = int(API_ID)
else:
    raise ValueError("API_ID environment variable is not set or invalid")

async def main():
    app = web.Application()
    # Your application setup code here
    # For example: app.router.add_get('/', handle)

    # Start your web server
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, 'localhost', 8080)
    await site.start()

if __name__ == "__main__":
    # Ensure environment variables are set and valid
    if not API_HASH or not BOT_TOKEN:
        raise ValueError("API_HASH or BOT_TOKEN environment variables are not set or invalid")
    
    asyncio.run(main())
