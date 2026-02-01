# 📦 Telegram File to Link Bot - Complete Package

## 🎉 What You Got

A **production-ready** Telegram bot that converts files (up to 4GB) into direct download and streaming links with premium subscription features!

## 📂 Project Structure

```
telegram_file_link_bot/
├── 📄 bot.py                    # Main bot launcher
├── ⚙️ config.py                 # All configurations
├── 💬 script.py                 # Bot messages & templates
├── 🛠️ utils.py                  # Helper functions
├── 📋 requirements.txt          # Python dependencies
├── 🔐 .env.example              # Environment template
├── 📖 README.md                 # Complete documentation
├── 🚀 SETUP_GUIDE.md            # Step-by-step setup
├── 🐳 Dockerfile                # Docker container config
├── 🐳 docker-compose.yml        # Docker compose config
├── 📝 .gitignore                # Git ignore rules
├── ▶️ startup.sh                # Quick start script
│
├── 📁 database/
│   ├── __init__.py
│   └── users_chats_db.py        # MongoDB operations
│
└── 📁 plugins/
    ├── __init__.py
    ├── start.py                 # Start command & force subscribe
    ├── file_handler.py          # File upload & link generation  
    ├── premium.py               # Premium features & Star payments
    ├── settings.py              # User settings & thumbnails
    ├── broadcast.py             # Admin broadcast tools
    └── ban.py                   # User/group ban management
```

## ✨ Features Implemented

### 🆓 Free User Features
✅ Upload files up to 4GB
✅ Stream & Download links
✅ 24-hour link validity
✅ 512 KB/s download speed
✅ AdFly monetization
✅ Force subscribe system
✅ Time-based greetings (India/Sri Lanka timezone)
✅ Random anime wallpapers on welcome
✅ Animated start (⏳ emoji for 2 seconds)

### 💎 Premium User Features
✅ Permanent links (never expire)
✅ Unlimited download speed
✅ Custom thumbnails
✅ No advertisements
✅ Priority support
✅ All free features

### 👨‍💼 Admin Features
✅ Broadcast to all users
✅ Broadcast to all groups
✅ Add/remove premium subscriptions
✅ List premium users
✅ Ban/unban users
✅ Disable groups
✅ Clean junk users/groups
✅ Star payment integration

### 🔧 Technical Features
✅ MongoDB database integration
✅ Force subscribe to multiple channels
✅ AdFly API integration (pre-configured)
✅ Progress tracking for uploads
✅ File metadata storage
✅ JSON data structure
✅ Docker support
✅ Environment-based configuration
✅ Modular plugin system
✅ Error handling & logging

## 💳 Payment Integration

**Telegram Star Payments** fully configured:
- 1 Month → 50⭐
- 3 Months → 100⭐
- 6 Months → 200⭐  
- 1 Year → 350⭐

**AdFly Monetization** included:
- API Key: `9a4803974a9dc9c639002d42c5a67f7c18961c0e`
- All download links are monetized
- Premium users get direct links

## 🎨 Customization Points

### Messages (script.py)
- Welcome message
- Help text
- About section
- Premium info
- Force subscribe message
- All user-facing text

### Settings (config.py)
- Force subscribe channels (default: @zerodev2, @mvxyoffcail)
- File size limits (default: 4GB)
- Link expiry times (free: 24h, premium: permanent)
- Download speed limits (free: 512KB/s, premium: unlimited)
- Premium plans & pricing
- AdFly API settings
- Timezone settings

### Images
- Force subscribe image: `https://i.ibb.co/pr2H8cwT/img-8312532076.jpg`
- Random anime API: `https://api.aniwallpaper.workers.dev/random?type=girl`
- Subscription image: Configurable in config.py

## 🚀 Quick Start (3 Steps)

### Step 1: Get Credentials
- Bot Token from @BotFather
- API ID & Hash from my.telegram.org
- MongoDB connection string
- Create bin channel & premium logs channel
- Get your user ID

### Step 2: Configure
```bash
cp .env.example .env
# Edit .env with your credentials
```

### Step 3: Run
```bash
chmod +x startup.sh
./startup.sh
```

**OR with Docker:**
```bash
docker-compose up -d
```

## 📋 Command Reference

### User Commands
```
/start      - Start the bot
/help       - Show help
/myplan     - Check premium status
/addthum    - Add thumbnail (Premium)
/viewthum   - View thumbnail
/delthum    - Delete thumbnail
/settings   - Configure settings
```

### Admin Commands
```
/broadcast user_message         - Broadcast to users
/grp_broadcast group_message    - Broadcast to groups
/add_premium user_id 1 month    - Add premium
/remove_premium user_id         - Remove premium
/get_premium user_id            - Check premium info
/premium_users                  - List premium users
/banned                         - List banned users
/clear_junk                     - Clean database
/clear_junk_group               - Clean group database
```

## 🔐 Security Features

✅ Admin-only commands protected
✅ User ban system
✅ Group disable system
✅ Force subscribe verification
✅ Database validation
✅ Error handling & logging
✅ File size validation
✅ Premium status verification

## 📊 Database Schema

### Users Collection
```python
{
    "id": user_id,
    "join_date": "2025-01-01",
    "ban_status": {"is_banned": False, "ban_reason": ""},
    "expiry_time": datetime or None,
    "thumbnail": file_id or None,
    "upload_mode": "document" or "video"
}
```

### Files Collection
```python
{
    "user_id": user_id,
    "message_id": message_id,
    "file_name": "filename.ext",
    "file_size": 123456789,
    "file_type": "document/video/audio",
    "is_premium": True/False,
    "stream_link": "shortened_url",
    "download_link": "shortened_url",
    "created_at": datetime
}
```

## 🌟 Unique Features

1. **Time-Based Greetings**: Shows good morning/afternoon/evening/night based on India/Sri Lanka timezone
2. **Animated Start**: ⏳ emoji appears for 2 seconds then auto-deletes
3. **Random Anime Wallpapers**: Each welcome message shows different anime wallpaper
4. **AdFly Integration**: Automatic link monetization for free users
5. **Star Payments**: Native Telegram payment integration
6. **Progressive Upload**: Real-time progress bar for file uploads
7. **Smart Link Management**: Automatic expiry for free users, permanent for premium
8. **Thumbnail Support**: Premium users can set custom video thumbnails
9. **Force Subscribe**: Multi-channel requirement system
10. **Modular Design**: Easy to add new features

## 🛠️ Tech Stack

- **Language**: Python 3.9+
- **Framework**: Pyrogram (Telegram MTProto)
- **Database**: MongoDB (Motor async driver)
- **Payment**: Telegram Stars
- **Monetization**: AdFly API
- **Deployment**: Docker, Heroku, VPS
- **Timezone**: pytz (Asia/Kolkata)

## 📈 Scalability

✅ Async/await throughout
✅ Batch processing for broadcasts
✅ Database indexing ready
✅ Rate limiting handled
✅ Error recovery mechanisms
✅ Resource cleanup
✅ Modular architecture

## 🐛 Error Handling

✅ Try-except blocks on all operations
✅ Logging system configured
✅ User-friendly error messages
✅ Admin error notifications
✅ Graceful degradation
✅ Timeout handling

## 📝 Environment Variables

Required in `.env` file:
```env
BOT_TOKEN=            # From @BotFather
API_ID=               # From my.telegram.org
API_HASH=             # From my.telegram.org
DATABASE_URI=         # MongoDB connection string
DATABASE_NAME=        # Database name (default: FileToLink)
ADMINS=               # Space-separated user IDs
BIN_CHANNEL=          # Channel ID for file storage
PREMIUM_LOGS=         # Channel ID for premium logs
```

## 🎯 Ready to Deploy On

✅ **Heroku** - Config vars + GitHub deploy
✅ **Railway** - One-click deploy
✅ **Render** - Auto deploy from Git
✅ **VPS** - systemd service or screen
✅ **Docker** - docker-compose up -d
✅ **Local** - python bot.py

## 💡 Pro Tips

1. **Enable Star Payments**: Go to @BotFather → /mybots → Your Bot → Payments → Telegram Stars
2. **Customize Force Sub**: Edit FORCE_SUB_CHANNELS in config.py
3. **Change Messages**: Edit script.py for all text customization
4. **Monitor Database**: Keep eye on MongoDB usage
5. **Backup Regularly**: Export database and configuration
6. **Update Channels**: Change @zerodev2 and @mvxyoffcail to your channels
7. **Test Everything**: Use /start, upload files, test premium before going live

## 📞 Support & Credits

- **Developer**: [@Venuboyy](https://t.me/Venuboyy)
- **Channel 1**: [@zerodev2](https://t.me/zerodev2)
- **Channel 2**: [@mvxyoffcail](https://t.me/mvxyoffcail)
- **Created by**: Zerodev
- **Version**: 1.0
- **License**: Educational Use

## ✅ What's Next?

1. Read **SETUP_GUIDE.md** for detailed setup instructions
2. Read **README.md** for comprehensive documentation
3. Configure your `.env` file
4. Run `python bot.py` or `./startup.sh`
5. Test all features
6. Customize to your needs
7. Deploy and share!

---

## 🎁 Bonus Features Included

✅ Docker support (Dockerfile + docker-compose.yml)
✅ Startup script (startup.sh)
✅ Complete documentation
✅ Example configuration (.env.example)
✅ Git ignore rules (.gitignore)
✅ Pre-configured AdFly API
✅ India/Sri Lanka timezone support
✅ Random anime wallpaper API
✅ Animated UI elements
✅ Professional error handling
✅ Production-ready code structure

---

**Everything is ready to use! Just configure and deploy!** 🚀

Made with ❤️ by Zerodev
