import asyncio
import logging
from pyrogram import Client
from config import API_ID, API_HASH, BOT_TOKEN
from database.users_chats_db import db
from utils import temp
from server import start_server

# Configure logging
logging.basicConfig(
    format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s',
    level=logging.INFO
)

# Initialize bot
class Bot(Client):
    def __init__(self):
        super().__init__(
            name="FileToLinkBot",
            api_id=API_ID,
            api_hash=API_HASH,
            bot_token=BOT_TOKEN,
            plugins=dict(root="plugins"),
            sleep_threshold=30
        )
        self.server_runner = None

    async def start(self):
        await super().start()
        me = await self.get_me()
        temp.ME = me
        
        # Load banned users and chats
        banned_users, banned_chats = await db.get_banned()
        temp.BANNED_USERS = banned_users
        temp.BANNED_CHATS = banned_chats
        
        # Start web server
        port = int(os.environ.get("PORT", 8080))
        self.server_runner = await start_server(port)
        
        logging.info(f"Bot started as @{me.username}")
        print(f"""
╔══════════════════════════════════════╗
║                                      ║
║      FILE TO LINK BOT STARTED!       ║
║                                      ║
║  Bot Username: @{me.username.ljust(20)}  ║
║  Bot ID: {str(me.id).ljust(26)}  ║
║  Web Server: Port {str(port).ljust(17)} ║
║                                      ║
║  Developer: @Venuboyy                ║
║  Version: 1.0                        ║
║                                      ║
╚══════════════════════════════════════╝
        """)

    async def stop(self, *args):
        if self.server_runner:
            from server import cleanup
            await cleanup(self.server_runner)
        await super().stop()
        logging.info("Bot stopped!")

# Run bot
if __name__ == "__main__":
    import os
    bot = Bot()
    bot.run()
