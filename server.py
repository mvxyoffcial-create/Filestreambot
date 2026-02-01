import os
import asyncio
from aiohttp import web
from pyrogram import Client
from database.users_chats_db import db
from config import BIN_CHANNEL, API_ID, API_HASH, BOT_TOKEN, FREE_USER_SPEED_LIMIT
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Global bot instance
bot = None

async def init_bot():
    """Initialize bot instance"""
    global bot
    if bot is None:
        bot = Client(
            "file_server",
            api_id=API_ID,
            api_hash=API_HASH,
            bot_token=BOT_TOKEN
        )
        await bot.start()
    return bot

async def stream_file(request):
    """Handle file streaming"""
    try:
        file_id = request.match_info.get('file_id')
        
        # Get file from database
        file_data = await db.get_file(file_id)
        
        if not file_data:
            return web.Response(text="File not found", status=404)
        
        # Check if file has expired
        if await db.check_file_expiry(file_id):
            return web.Response(text="Link expired. Please regenerate the link.", status=410)
        
        # Get bot instance
        client = await init_bot()
        
        # Get file from bin channel
        try:
            message = await client.get_messages(BIN_CHANNEL, file_data['message_id'])
            
            if not message:
                return web.Response(text="File not found in storage", status=404)
            
            # Get file
            if message.document:
                file = message.document
            elif message.video:
                file = message.video
            elif message.audio:
                file = message.audio
            else:
                return web.Response(text="Invalid file type", status=400)
            
            # Download file
            file_path = await client.download_media(
                message,
                file_name=file_data['file_name']
            )
            
            if not file_path or not os.path.exists(file_path):
                return web.Response(text="Error downloading file", status=500)
            
            # Stream file
            response = web.StreamResponse()
            response.headers['Content-Type'] = 'application/octet-stream'
            response.headers['Content-Disposition'] = f'inline; filename="{file_data["file_name"]}"'
            response.headers['Content-Length'] = str(os.path.getsize(file_path))
            
            await response.prepare(request)
            
            # Stream with speed limit for free users
            chunk_size = 64 * 1024  # 64KB chunks
            is_premium = file_data.get('is_premium', False)
            
            with open(file_path, 'rb') as f:
                while True:
                    chunk = f.read(chunk_size)
                    if not chunk:
                        break
                    
                    await response.write(chunk)
                    
                    # Apply speed limit for free users
                    if not is_premium and FREE_USER_SPEED_LIMIT:
                        await asyncio.sleep(chunk_size / FREE_USER_SPEED_LIMIT)
            
            await response.write_eof()
            
            # Clean up
            if os.path.exists(file_path):
                os.remove(file_path)
            
            return response
            
        except Exception as e:
            logger.error(f"Error streaming file: {e}")
            return web.Response(text="Error streaming file", status=500)
    
    except Exception as e:
        logger.error(f"Stream error: {e}")
        return web.Response(text="Internal server error", status=500)

async def download_file(request):
    """Handle file download"""
    try:
        file_id = request.match_info.get('file_id')
        
        # Get file from database
        file_data = await db.get_file(file_id)
        
        if not file_data:
            return web.Response(text="File not found", status=404)
        
        # Check if file has expired
        if await db.check_file_expiry(file_id):
            return web.Response(text="Link expired. Please regenerate the link.", status=410)
        
        # Get bot instance
        client = await init_bot()
        
        # Get file from bin channel
        try:
            message = await client.get_messages(BIN_CHANNEL, file_data['message_id'])
            
            if not message:
                return web.Response(text="File not found in storage", status=404)
            
            # Get file
            if message.document:
                file = message.document
            elif message.video:
                file = message.video
            elif message.audio:
                file = message.audio
            else:
                return web.Response(text="Invalid file type", status=400)
            
            # Download file
            file_path = await client.download_media(
                message,
                file_name=file_data['file_name']
            )
            
            if not file_path or not os.path.exists(file_path):
                return web.Response(text="Error downloading file", status=500)
            
            # Send file as download
            response = web.StreamResponse()
            response.headers['Content-Type'] = 'application/octet-stream'
            response.headers['Content-Disposition'] = f'attachment; filename="{file_data["file_name"]}"'
            response.headers['Content-Length'] = str(os.path.getsize(file_path))
            
            await response.prepare(request)
            
            # Stream with speed limit for free users
            chunk_size = 64 * 1024  # 64KB chunks
            is_premium = file_data.get('is_premium', False)
            
            with open(file_path, 'rb') as f:
                while True:
                    chunk = f.read(chunk_size)
                    if not chunk:
                        break
                    
                    await response.write(chunk)
                    
                    # Apply speed limit for free users
                    if not is_premium and FREE_USER_SPEED_LIMIT:
                        await asyncio.sleep(chunk_size / FREE_USER_SPEED_LIMIT)
            
            await response.write_eof()
            
            # Clean up
            if os.path.exists(file_path):
                os.remove(file_path)
            
            return response
            
        except Exception as e:
            logger.error(f"Error downloading file: {e}")
            return web.Response(text="Error downloading file", status=500)
    
    except Exception as e:
        logger.error(f"Download error: {e}")
        return web.Response(text="Internal server error", status=500)

async def health_check(request):
    """Health check endpoint"""
    return web.Response(text="OK", status=200)

def create_app():
    """Create web application"""
    app = web.Application(client_max_size=1024**3 * 5)  # 5GB max
    
    # Add routes
    app.router.add_get('/stream/{file_id}', stream_file)
    app.router.add_get('/download/{file_id}', download_file)
    app.router.add_get('/health', health_check)
    app.router.add_get('/', health_check)
    
    return app

async def start_server(port=8080):
    """Start web server"""
    app = create_app()
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, '0.0.0.0', port)
    await site.start()
    logger.info(f"Web server started on port {port}")
    return runner

async def cleanup(runner):
    """Cleanup on shutdown"""
    global bot
    await runner.cleanup()
    if bot:
        await bot.stop()
