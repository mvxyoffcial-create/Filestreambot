import time
import datetime
import math
import pytz
import requests
from pyrogram import enums
from config import ADFLY_API_KEY, ADFLY_API_URL

class temp:
    BANNED_USERS = []
    BANNED_CHATS = []
    B_USERS_CANCEL = False
    B_GROUPS_CANCEL = False
    B_LINK = ""
    ME = None
    SETTINGS = {}
    THUMBNAILS = {}

def get_readable_time(seconds: int) -> str:
    """Convert seconds to readable time format"""
    count = 0
    readable_time = ""
    time_list = []
    time_suffix_list = ["s", "m", "h", "days"]
    
    while count < 4:
        count += 1
        if count < 3:
            remainder, result = divmod(seconds, 60)
        else:
            remainder, result = divmod(seconds, 24)
        if seconds == 0 and remainder == 0:
            break
        time_list.append(int(result))
        seconds = int(remainder)
    
    for i in range(len(time_list)):
        time_list[i] = str(time_list[i]) + time_suffix_list[i]
    if len(time_list) == 4:
        readable_time += time_list.pop() + ", "
    
    time_list.reverse()
    readable_time += ":".join(time_list)
    
    return readable_time

def humanbytes(size):
    """Convert bytes to human readable format"""
    if not size:
        return "0B"
    power = 2**10
    n = 0
    Dic_powerN = {0: ' ', 1: 'Ki', 2: 'Mi', 3: 'Gi', 4: 'Ti'}
    while size > power:
        size /= power
        n += 1
    return f"{size:.2f} {Dic_powerN[n]}B"

async def get_seconds(time_str):
    """Convert time string to seconds"""
    try:
        time_value, time_unit = time_str.split()
        time_value = int(time_value)
        
        if 'min' in time_unit:
            return time_value * 60
        elif 'hour' in time_unit:
            return time_value * 3600
        elif 'day' in time_unit:
            return time_value * 86400
        elif 'month' in time_unit:
            return time_value * 2592000
        elif 'year' in time_unit:
            return time_value * 31536000
        else:
            return 0
    except:
        return 0

def get_greeting():
    """Get greeting based on time in Sri Lanka and India timezone"""
    # Both countries use UTC+5:30
    ist = pytz.timezone('Asia/Kolkata')
    current_time = datetime.datetime.now(ist)
    hour = current_time.hour
    
    if 5 <= hour < 12:
        return "🌅 ɢᴏᴏᴅ ᴍᴏʀɴɪɴɢ"
    elif 12 <= hour < 17:
        return "☀️ ɢᴏᴏᴅ ᴀғᴛᴇʀɴᴏᴏɴ"
    elif 17 <= hour < 21:
        return "🌆 ɢᴏᴏᴅ ᴇᴠᴇɴɪɴɢ"
    else:
        return "🌙 ɢᴏᴏᴅ ɴɪɢʜᴛ"

async def shorten_url(long_url, alias=None):
    """Shorten URL using AdFly API"""
    try:
        params = {
            'api': ADFLY_API_KEY,
            'url': long_url,
            'format': 'json'
        }
        
        if alias:
            params['alias'] = alias
        
        response = requests.get(ADFLY_API_URL, params=params, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            if data.get('status') == 'success':
                return data.get('shortenedUrl')
        
        return None
    except Exception as e:
        print(f"Error shortening URL: {e}")
        return None

async def users_broadcast(user_id, message, pin):
    """Broadcast message to user"""
    try:
        await message.copy(chat_id=user_id)
        if pin:
            try:
                await message.pin(chat_id=user_id, disable_notification=True)
            except:
                pass
        return True, "Success"
    except Exception as e:
        if "blocked" in str(e).lower():
            return False, "Blocked"
        elif "deleted" in str(e).lower() or "deactivated" in str(e).lower():
            return False, "Deleted"
        else:
            return False, "Error"

async def groups_broadcast(chat_id, message, pin):
    """Broadcast message to group"""
    try:
        await message.copy(chat_id=chat_id)
        if pin:
            try:
                await message.pin(chat_id=chat_id, disable_notification=True, both_sides=True)
            except:
                pass
        return "Success"
    except Exception as e:
        return "Error"

async def clear_junk(user_id, message):
    """Check if user is accessible"""
    try:
        await message._client.send_chat_action(user_id, enums.ChatAction.TYPING)
        return True, "Success"
    except Exception as e:
        if "blocked" in str(e).lower():
            return False, "Blocked"
        elif "deleted" in str(e).lower() or "deactivated" in str(e).lower():
            return False, "Deleted"
        else:
            return False, "Error"

async def junk_group(chat_id, message):
    """Check if group is accessible"""
    try:
        await message._client.send_chat_action(chat_id, enums.ChatAction.TYPING)
        return True, "success", ""
    except Exception as e:
        error = str(e)
        if "chat not found" in error.lower() or "chat_id_invalid" in error.lower():
            return False, "deleted", f"\n{chat_id} : {error}"
        else:
            return True, "success", ""

def time_formatter(milliseconds: int) -> str:
    """Format time from milliseconds"""
    seconds, milliseconds = divmod(int(milliseconds), 1000)
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    days, hours = divmod(hours, 24)
    tmp = ((str(days) + "d, ") if days else "") + \
        ((str(hours) + "h, ") if hours else "") + \
        ((str(minutes) + "m, ") if minutes else "") + \
        ((str(seconds) + "s, ") if seconds else "")
    return tmp[:-2]

def size_formatter(b: int) -> str:
    """Format size in bytes to readable format"""
    if not b:
        return "0B"
    l = ["B", "KB", "MB", "GB", "TB", "PB"]
    e = 0
    while b >= 1024 and e < len(l) - 1:
        b /= 1024
        e += 1
    return f"{b:.2f}{l[e]}"
