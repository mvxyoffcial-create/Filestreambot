import asyncio
import requests
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.errors import UserNotParticipant
from database.users_chats_db import db
from script import script
from config import FORCE_SUB_CHANNELS, FORCE_SUB_IMAGE, RANDOM_ANIME_API, OWNER
from utils import get_greeting, temp

@Client.on_message(filters.command("start") & filters.private)
async def start_command(client, message):
    user_id = message.from_user.id
    
    # Check force subscribe
    not_joined = []
    for channel in FORCE_SUB_CHANNELS:
        try:
            await client.get_chat_member(f"@{channel}", user_id)
        except UserNotParticipant:
            not_joined.append(channel)
        except Exception:
            pass
    
    if not_joined:
        buttons = []
        for i, channel in enumerate(not_joined, 1):
            buttons.append([InlineKeyboardButton(f"📢 ᴊᴏɪɴ ᴄʜᴀɴɴᴇʟ {i}", url=f"https://t.me/{channel}")])
        buttons.append([InlineKeyboardButton("✅ ɪ ᴊᴏɪɴᴇᴅ", callback_data="check_joined")])
        
        await message.reply_photo(
            photo=FORCE_SUB_IMAGE,
            caption=script.FORCE_SUB_TEXT.format(message.from_user.mention),
            reply_markup=InlineKeyboardMarkup(buttons)
        )
        return
    
    # Show animated hourglass emoji
    loading_msg = await message.reply("⚡")
    await asyncio.sleep(2)
    await loading_msg.delete()
    
    # Add user to database if new
    if not await db.is_user_exist(user_id):
        await db.add_user(user_id)
    
    # Get random anime wallpaper
    try:
        response = requests.get(RANDOM_ANIME_API, timeout=5)
        if response.status_code == 200:
            data = response.json()
            photo_url = data.get('url', 'https://i.ibb.co/pr2H8cwT/img-8312532076.jpg')
        else:
            photo_url = 'https://i.ibb.co/pr2H8cwT/img-8312532076.jpg'
    except:
        photo_url = 'https://i.ibb.co/pr2H8cwT/img-8312532076.jpg'
    
    greeting = get_greeting()
    
    buttons = [
        [
            InlineKeyboardButton("📚 ʜᴇʟᴘ", callback_data="help"),
            InlineKeyboardButton("ℹ️ ᴀʙᴏᴜᴛ", callback_data="about")
        ],
        [
            InlineKeyboardButton("💎 ᴘʀᴇᴍɪᴜᴍ", callback_data="premium_info"),
            InlineKeyboardButton("⚙️ sᴇᴛᴛɪɴɢs", callback_data="settings")
        ],
        [
            InlineKeyboardButton("👨‍💻 ᴅᴇᴠᴇʟᴏᴘᴇʀ", url=f"https://t.me/{OWNER.replace('@', '')}")
        ]
    ]
    
    await message.reply_photo(
        photo=photo_url,
        caption=script.START_TXT.format(message.from_user.mention, greeting),
        reply_markup=InlineKeyboardMarkup(buttons)
    )

@Client.on_message(filters.command("start") & filters.group)
async def group_start(client, message):
    buttons = [
        [
            InlineKeyboardButton("📚 ʜᴇʟᴘ", callback_data="help"),
            InlineKeyboardButton("💎 ᴘʀᴇᴍɪᴜᴍ", callback_data="premium_info")
        ]
    ]
    
    greeting = get_greeting()
    
    await message.reply_text(
        script.GSTART_TXT.format(message.from_user.mention, greeting),
        reply_markup=InlineKeyboardMarkup(buttons)
    )
    
    # Add group to database
    if not await db.is_chat_exist(message.chat.id):
        await db.add_chat(message.chat.id)

@Client.on_callback_query(filters.regex("^check_joined$"))
async def check_joined_callback(client, callback_query):
    user_id = callback_query.from_user.id
    
    # Check force subscribe again
    not_joined = []
    for channel in FORCE_SUB_CHANNELS:
        try:
            await client.get_chat_member(f"@{channel}", user_id)
        except UserNotParticipant:
            not_joined.append(channel)
        except Exception:
            pass
    
    if not_joined:
        await callback_query.answer("❌ ʏᴏᴜ ʜᴀᴠᴇɴ'ᴛ ᴊᴏɪɴᴇᴅ ᴀʟʟ ᴄʜᴀɴɴᴇʟs ʏᴇᴛ!", show_alert=True)
        return
    
    await callback_query.message.delete()
    
    # Add user to database
    if not await db.is_user_exist(user_id):
        await db.add_user(user_id)
    
    # Get random anime wallpaper
    try:
        response = requests.get(RANDOM_ANIME_API, timeout=5)
        if response.status_code == 200:
            data = response.json()
            photo_url = data.get('url', 'https://i.ibb.co/pr2H8cwT/img-8312532076.jpg')
        else:
            photo_url = 'https://i.ibb.co/pr2H8cwT/img-8312532076.jpg'
    except:
        photo_url = 'https://i.ibb.co/pr2H8cwT/img-8312532076.jpg'
    
    greeting = get_greeting()
    
    buttons = [
        [
            InlineKeyboardButton("📚 ʜᴇʟᴘ", callback_data="help"),
            InlineKeyboardButton("ℹ️ ᴀʙᴏᴜᴛ", callback_data="about")
        ],
        [
            InlineKeyboardButton("💎 ᴘʀᴇᴍɪᴜᴍ", callback_data="premium_info"),
            InlineKeyboardButton("⚙️ sᴇᴛᴛɪɴɢs", callback_data="settings")
        ],
        [
            InlineKeyboardButton("👨‍💻 ᴅᴇᴠᴇʟᴏᴘᴇʀ", url=f"https://t.me/{OWNER.replace('@', '')}")
        ]
    ]
    
    await callback_query.message.reply_photo(
        photo=photo_url,
        caption=script.START_TXT.format(callback_query.from_user.mention, greeting),
        reply_markup=InlineKeyboardMarkup(buttons)
    )

@Client.on_callback_query(filters.regex("^help$"))
async def help_callback(client, callback_query):
    buttons = [
        [InlineKeyboardButton("🔙 ʙᴀᴄᴋ", callback_data="start")]
    ]
    
    await callback_query.message.edit_text(
        script.HELP_TXT,
        reply_markup=InlineKeyboardMarkup(buttons)
    )

@Client.on_callback_query(filters.regex("^about$"))
async def about_callback(client, callback_query):
    buttons = [
        [InlineKeyboardButton("🔙 ʙᴀᴄᴋ", callback_data="start")]
    ]
    
    me = await client.get_me()
    
    await callback_query.message.edit_text(
        script.ABOUT_TXT.format(me.username, me.first_name, f"https://t.me/{OWNER.replace('@', '')}"),
        reply_markup=InlineKeyboardMarkup(buttons),
        disable_web_page_preview=True
    )

@Client.on_callback_query(filters.regex("^start$"))
async def start_callback(client, callback_query):
    greeting = get_greeting()
    
    buttons = [
        [
            InlineKeyboardButton("📚 ʜᴇʟᴘ", callback_data="help"),
            InlineKeyboardButton("ℹ️ ᴀʙᴏᴜᴛ", callback_data="about")
        ],
        [
            InlineKeyboardButton("💎 ᴘʀᴇᴍɪᴜᴍ", callback_data="premium_info"),
            InlineKeyboardButton("⚙️ sᴇᴛᴛɪɴɢs", callback_data="settings")
        ],
        [
            InlineKeyboardButton("👨‍💻 ᴅᴇᴠᴇʟᴏᴘᴇʀ", url=f"https://t.me/{OWNER.replace('@', '')}")
        ]
    ]
    
    await callback_query.message.edit_text(
        script.START_TXT.format(callback_query.from_user.mention, greeting),
        reply_markup=InlineKeyboardMarkup(buttons)
    )

@Client.on_callback_query(filters.regex("^close_data$"))
async def close_callback(client, callback_query):
    await callback_query.message.delete()
