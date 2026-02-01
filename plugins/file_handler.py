import os
import time
import datetime
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from database.users_chats_db import db
from config import BIN_CHANNEL, MAX_FILE_SIZE, FREE_USER_LINK_EXPIRY
from utils import humanbytes, shorten_url, temp

# Dictionary to store upload progress
upload_progress = {}

async def progress_callback(current, total, message, start_time, user_id):
    """Progress callback for file upload"""
    now = time.time()
    diff = now - start_time
    
    if user_id in upload_progress:
        last_update = upload_progress[user_id]
        if now - last_update < 3:  # Update every 3 seconds
            return
    
    upload_progress[user_id] = now
    
    percentage = current * 100 / total
    speed = current / diff
    elapsed_time = round(diff)
    
    if current == total:
        eta = 0
    else:
        eta = round((total - current) / speed)
    
    # Format progress bar
    filled = int(percentage / 5)
    bar = '█' * filled + '░' * (20 - filled)
    
    try:
        await message.edit_text(
            f"📤 **ᴜᴘʟᴏᴀᴅɪɴɢ...**\n\n"
            f"`{bar}` {percentage:.1f}%\n\n"
            f"**📊 sɪᴢᴇ:** {humanbytes(current)} / {humanbytes(total)}\n"
            f"**⚡ sᴘᴇᴇᴅ:** {humanbytes(speed)}/s\n"
            f"**⏱️ ᴇʟᴀᴘsᴇᴅ:** {elapsed_time}s\n"
            f"**⏳ ᴇᴛᴀ:** {eta}s"
        )
    except:
        pass

@Client.on_message(filters.private & (filters.document | filters.video | filters.audio))
async def handle_file(client, message):
    user_id = message.from_user.id
    
    # Check if user is banned
    ban_status = await db.get_ban_status(user_id)
    if ban_status['is_banned']:
        await message.reply_text(
            f"❌ **sᴏʀʀʏ, ʏᴏᴜ ᴀʀᴇ ʙᴀɴɴᴇᴅ!**\n\n"
            f"**ʀᴇᴀsᴏɴ:** {ban_status['ban_reason']}"
        )
        return
    
    # Add user to database if new
    if not await db.is_user_exist(user_id):
        await db.add_user(user_id)
    
    # Get file info
    file = message.document or message.video or message.audio
    file_size = file.file_size
    
    # Check file size limit
    if file_size > MAX_FILE_SIZE:
        await message.reply_text(
            f"❌ **ғɪʟᴇ ᴛᴏᴏ ʟᴀʀɢᴇ!**\n\n"
            f"**ᴍᴀx ғɪʟᴇ sɪᴢᴇ:** {humanbytes(MAX_FILE_SIZE)}\n"
            f"**ʏᴏᴜʀ ғɪʟᴇ:** {humanbytes(file_size)}"
        )
        return
    
    # Check if user is premium
    is_premium = await db.check_premium(user_id)
    
    # Get user's thumbnail
    thumbnail = await db.get_thumbnail(user_id)
    
    # Get upload mode
    upload_mode = await db.get_upload_mode(user_id)
    
    # Start upload
    status_msg = await message.reply_text("⏳ **ᴘʀᴏᴄᴇssɪɴɢ ʏᴏᴜʀ ғɪʟᴇ...**")
    
    try:
        start_time = time.time()
        
        # Upload to bin channel
        if message.document:
            sent_file = await message.copy(
                chat_id=BIN_CHANNEL,
                caption=f"**ᴜsᴇʀ:** {message.from_user.mention}\n**ᴜsᴇʀ ɪᴅ:** `{user_id}`\n**ғɪʟᴇ ɴᴀᴍᴇ:** `{file.file_name}`\n**sɪᴢᴇ:** {humanbytes(file_size)}"
            )
        elif message.video:
            if thumbnail:
                # Download thumbnail
                thumb_path = await client.download_media(thumbnail)
                sent_file = await client.send_video(
                    chat_id=BIN_CHANNEL,
                    video=message.video.file_id,
                    caption=f"**ᴜsᴇʀ:** {message.from_user.mention}\n**ᴜsᴇʀ ɪᴅ:** `{user_id}`\n**ғɪʟᴇ ɴᴀᴍᴇ:** `{file.file_name}`\n**sɪᴢᴇ:** {humanbytes(file_size)}",
                    thumb=thumb_path,
                    progress=progress_callback,
                    progress_args=(status_msg, start_time, user_id)
                )
                if os.path.exists(thumb_path):
                    os.remove(thumb_path)
            else:
                sent_file = await message.copy(
                    chat_id=BIN_CHANNEL,
                    caption=f"**ᴜsᴇʀ:** {message.from_user.mention}\n**ᴜsᴇʀ ɪᴅ:** `{user_id}`\n**ғɪʟᴇ ɴᴀᴍᴇ:** `{file.file_name}`\n**sɪᴢᴇ:** {humanbytes(file_size)}"
                )
        else:
            sent_file = await message.copy(
                chat_id=BIN_CHANNEL,
                caption=f"**ᴜsᴇʀ:** {message.from_user.mention}\n**ᴜsᴇʀ ɪᴅ:** `{user_id}`\n**ғɪʟᴇ ɴᴀᴍᴇ:** `{file.file_name}`\n**sɪᴢᴇ:** {humanbytes(file_size)}"
            )
        
        # Clean up progress tracker
        if user_id in upload_progress:
            del upload_progress[user_id]
        
        # Save file data to database
        file_data = {
            'user_id': user_id,
            'message_id': sent_file.id,
            'file_name': file.file_name,
            'file_size': file_size,
            'file_type': 'document' if message.document else 'video' if message.video else 'audio',
            'is_premium': is_premium,
            'created_at': datetime.datetime.now()
        }
        
        file_id = await db.save_file(file_data)
        
        # Generate links
        from config import BASE_URL
        stream_link = f"{BASE_URL}/stream/{file_id}"
        download_link = f"{BASE_URL}/download/{file_id}"
        
        # Shorten links using AdFly (only for free users)
        if is_premium:
            # Premium users get direct links
            short_stream = stream_link
            short_download = download_link
        else:
            # Free users get AdFly monetized links
            short_stream = await shorten_url(stream_link) or stream_link
            short_download = await shorten_url(download_link) or download_link
        
        # Update database with links
        await db.update_file_links(file_id, short_stream, short_download)
        
        # Create response message
        expiry_text = "♾️ **ᴘᴇʀᴍᴀɴᴇɴᴛ**" if is_premium else "24 ʜᴏᴜʀs ⏰"
        speed_text = "**ᴜɴʟɪᴍɪᴛᴇᴅ** ⚡" if is_premium else "**512 ᴋʙ/s** 🐢"
        
        caption = (
            f"✅ **ʏᴏᴜʀ ғɪʟᴇ ɪs ʀᴇᴀᴅʏ!**\n\n"
            f"📁 **ғɪʟᴇ ɴᴀᴍᴇ:** `{file.file_name}`\n"
            f"📊 **sɪᴢᴇ:** {humanbytes(file_size)}\n"
            f"⏳ **ᴇxᴘɪʀʏ:** {expiry_text}\n"
            f"⚡ **sᴘᴇᴇᴅ:** {speed_text}\n\n"
            f"{'💎 **ᴘʀᴇᴍɪᴜᴍ ᴜsᴇʀ**' if is_premium else '🆓 **ғʀᴇᴇ ᴜsᴇʀ**'}"
        )
        
        buttons = [
            [
                InlineKeyboardButton("🎬 sᴛʀᴇᴀᴍ", url=short_stream),
                InlineKeyboardButton("📥 ᴅᴏᴡɴʟᴏᴀᴅ", url=short_download)
            ]
        ]
        
        if not is_premium:
            buttons.append([InlineKeyboardButton("💎 ɢᴇᴛ ᴘʀᴇᴍɪᴜᴍ", callback_data="premium_info")])
        
        buttons.append([InlineKeyboardButton("❌ ᴄʟᴏsᴇ", callback_data="close_data")])
        
        await status_msg.edit_text(
            caption,
            reply_markup=InlineKeyboardMarkup(buttons)
        )
        
    except Exception as e:
        print(f"Error handling file: {e}")
        await status_msg.edit_text(
            f"❌ **ᴇʀʀᴏʀ ᴘʀᴏᴄᴇssɪɴɢ ғɪʟᴇ!**\n\n"
            f"**ᴇʀʀᴏʀ:** `{str(e)}`"
        )
        if user_id in upload_progress:
            del upload_progress[user_id]
