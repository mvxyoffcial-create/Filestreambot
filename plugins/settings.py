from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from database.users_chats_db import db
from script import script

@Client.on_message(filters.command("addthum") & filters.private)
async def add_thumbnail(client, message):
    """Add custom thumbnail"""
    user_id = message.from_user.id
    
    # Check if user is premium
    is_premium = await db.check_premium(user_id)
    
    if not is_premium:
        await message.reply_text(
            "❌ **ᴘʀᴇᴍɪᴜᴍ ғᴇᴀᴛᴜʀᴇ!**\n\n"
            "ᴄᴜsᴛᴏᴍ ᴛʜᴜᴍʙɴᴀɪʟs ᴀʀᴇ ᴏɴʟʏ ᴀᴠᴀɪʟᴀʙʟᴇ ғᴏʀ ᴘʀᴇᴍɪᴜᴍ ᴜsᴇʀs! 💎",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("💎 ɢᴇᴛ ᴘʀᴇᴍɪᴜᴍ", callback_data="premium_info")]
            ])
        )
        return
    
    reply = message.reply_to_message
    
    if not reply:
        await message.reply_text("❌ **ᴘʟᴇᴀsᴇ ʀᴇᴘʟʏ ᴛᴏ ᴀ ᴘʜᴏᴛᴏ!**")
        return
    
    if not reply.photo:
        await message.reply_text("❌ **ᴛʜɪs ɪs ɴᴏᴛ ᴀ ᴘʜᴏᴛᴏ!**")
        return
    
    # Save thumbnail
    await db.set_thumbnail(user_id, reply.photo.file_id)
    await message.reply_text(
        "✅ **ᴛʜᴜᴍʙɴᴀɪʟ sᴀᴠᴇᴅ sᴜᴄᴄᴇssғᴜʟʟʏ!**\n\n"
        "ʏᴏᴜʀ ᴄᴜsᴛᴏᴍ ᴛʜᴜᴍʙɴᴀɪʟ ᴡɪʟʟ ʙᴇ ᴜsᴇᴅ ғᴏʀ ᴀʟʟ ʏᴏᴜʀ ᴠɪᴅᴇᴏs! 🎬"
    )

@Client.on_message(filters.command("viewthum") & filters.private)
async def view_thumbnail(client, message):
    """View current thumbnail"""
    user_id = message.from_user.id
    
    thumbnail = await db.get_thumbnail(user_id)
    
    if not thumbnail:
        await message.reply_text(
            "❌ **ɴᴏ ᴛʜᴜᴍʙɴᴀɪʟ sᴇᴛ!**\n\n"
            "ᴜsᴇ /addthum ᴛᴏ sᴇᴛ ᴀ ᴄᴜsᴛᴏᴍ ᴛʜᴜᴍʙɴᴀɪʟ."
        )
        return
    
    await message.reply_photo(
        photo=thumbnail,
        caption="🖼️ **ʏᴏᴜʀ ᴄᴜʀʀᴇɴᴛ ᴛʜᴜᴍʙɴᴀɪʟ**"
    )

@Client.on_message(filters.command("delthum") & filters.private)
async def delete_thumbnail(client, message):
    """Delete thumbnail"""
    user_id = message.from_user.id
    
    thumbnail = await db.get_thumbnail(user_id)
    
    if not thumbnail:
        await message.reply_text("❌ **ɴᴏ ᴛʜᴜᴍʙɴᴀɪʟ ᴛᴏ ᴅᴇʟᴇᴛᴇ!**")
        return
    
    await db.delete_thumbnail(user_id)
    await message.reply_text("✅ **ᴛʜᴜᴍʙɴᴀɪʟ ᴅᴇʟᴇᴛᴇᴅ sᴜᴄᴄᴇssғᴜʟʟʏ!**")

@Client.on_callback_query(filters.regex("^settings$"))
async def settings_callback(client, callback_query):
    """Show settings menu"""
    user_id = callback_query.from_user.id
    
    # Get current settings
    upload_mode = await db.get_upload_mode(user_id)
    thumbnail = await db.get_thumbnail(user_id)
    
    mode_text = "📄 **ᴅᴏᴄᴜᴍᴇɴᴛ**" if upload_mode == "document" else "🎬 **ᴠɪᴅᴇᴏ**"
    thumb_text = "✅ **sᴇᴛ**" if thumbnail else "❌ **ɴᴏᴛ sᴇᴛ**"
    
    buttons = [
        [
            InlineKeyboardButton(
                "📄 ᴅᴏᴄᴜᴍᴇɴᴛ" if upload_mode == "video" else "✅ ᴅᴏᴄᴜᴍᴇɴᴛ",
                callback_data="set_mode_document"
            ),
            InlineKeyboardButton(
                "🎬 ᴠɪᴅᴇᴏ" if upload_mode == "document" else "✅ ᴠɪᴅᴇᴏ",
                callback_data="set_mode_video"
            )
        ],
        [
            InlineKeyboardButton("🖼️ ᴛʜᴜᴍʙɴᴀɪʟ sᴇᴛᴛɪɴɢs", callback_data="thumbnail_settings")
        ],
        [
            InlineKeyboardButton("🔙 ʙᴀᴄᴋ", callback_data="start")
        ]
    ]
    
    await callback_query.message.edit_text(
        script.SETTINGS_TEXT.format(mode_text, thumb_text),
        reply_markup=InlineKeyboardMarkup(buttons)
    )

@Client.on_callback_query(filters.regex("^set_mode_"))
async def set_upload_mode(client, callback_query):
    """Set upload mode"""
    user_id = callback_query.from_user.id
    mode = callback_query.data.split("_")[2]
    
    await db.set_upload_mode(user_id, mode)
    
    # Refresh settings
    upload_mode = await db.get_upload_mode(user_id)
    thumbnail = await db.get_thumbnail(user_id)
    
    mode_text = "📄 **ᴅᴏᴄᴜᴍᴇɴᴛ**" if upload_mode == "document" else "🎬 **ᴠɪᴅᴇᴏ**"
    thumb_text = "✅ **sᴇᴛ**" if thumbnail else "❌ **ɴᴏᴛ sᴇᴛ**"
    
    buttons = [
        [
            InlineKeyboardButton(
                "📄 ᴅᴏᴄᴜᴍᴇɴᴛ" if upload_mode == "video" else "✅ ᴅᴏᴄᴜᴍᴇɴᴛ",
                callback_data="set_mode_document"
            ),
            InlineKeyboardButton(
                "🎬 ᴠɪᴅᴇᴏ" if upload_mode == "document" else "✅ ᴠɪᴅᴇᴏ",
                callback_data="set_mode_video"
            )
        ],
        [
            InlineKeyboardButton("🖼️ ᴛʜᴜᴍʙɴᴀɪʟ sᴇᴛᴛɪɴɢs", callback_data="thumbnail_settings")
        ],
        [
            InlineKeyboardButton("🔙 ʙᴀᴄᴋ", callback_data="start")
        ]
    ]
    
    await callback_query.message.edit_text(
        script.SETTINGS_TEXT.format(mode_text, thumb_text),
        reply_markup=InlineKeyboardMarkup(buttons)
    )
    
    await callback_query.answer(f"✅ ᴜᴘʟᴏᴀᴅ ᴍᴏᴅᴇ sᴇᴛ ᴛᴏ {mode.upper()}", show_alert=True)

@Client.on_callback_query(filters.regex("^thumbnail_settings$"))
async def thumbnail_settings(client, callback_query):
    """Show thumbnail settings"""
    user_id = callback_query.from_user.id
    
    is_premium = await db.check_premium(user_id)
    thumbnail = await db.get_thumbnail(user_id)
    
    if not is_premium:
        await callback_query.answer(
            "❌ ᴘʀᴇᴍɪᴜᴍ ғᴇᴀᴛᴜʀᴇ!\n\nᴄᴜsᴛᴏᴍ ᴛʜᴜᴍʙɴᴀɪʟs ᴀʀᴇ ᴏɴʟʏ ᴀᴠᴀɪʟᴀʙʟᴇ ғᴏʀ ᴘʀᴇᴍɪᴜᴍ ᴜsᴇʀs!",
            show_alert=True
        )
        return
    
    status_text = "✅ **sᴇᴛ**" if thumbnail else "❌ **ɴᴏᴛ sᴇᴛ**"
    
    buttons = [
        [InlineKeyboardButton("🔙 ʙᴀᴄᴋ", callback_data="settings")]
    ]
    
    await callback_query.message.edit_text(
        script.THUMBNAIL_TEXT.format(status_text),
        reply_markup=InlineKeyboardMarkup(buttons)
    )
