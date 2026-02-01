# 🚀 Telegram File to Link Bot

A powerful Telegram bot that converts files up to 4GB into direct download and streaming links with premium features and AdFly monetization.

## ✨ Features

### 🆓 Free Users
- ✅ Upload files up to 4GB
- ✅ Generate download & stream links
- ✅ Links valid for 24 hours
- ✅ Download speed: 512 KB/s
- ✅ AdFly monetization on links

### 💎 Premium Users
- ✅ Upload files up to 4GB
- ✅ Permanent links (never expire)
- ✅ Unlimited download speed
- ✅ Custom thumbnails
- ✅ No advertisements
- ✅ Priority support

## 📋 Requirements

- Python 3.9+
- MongoDB Database
- Telegram Bot Token
- Telegram API ID & API Hash
- AdFly API Key (already configured)

## 🛠️ Installation

### 1. Clone Repository

```bash
git clone https://github.com/yourusername/file-to-link-bot
cd file-to-link-bot
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configuration

1. Copy the `.env.example` file to `.env`:
```bash
cp .env.example .env
```

2. Edit `.env` with your credentials:

```env
BOT_TOKEN=your_bot_token_from_@BotFather
API_ID=your_api_id_from_my.telegram.org
API_HASH=your_api_hash_from_my.telegram.org
DATABASE_URI=your_mongodb_connection_string
DATABASE_NAME=FileToLink
ADMINS=your_telegram_user_id another_admin_id
BIN_CHANNEL=-100xxxxxxxxxx  # Channel ID where files will be stored
PREMIUM_LOGS=-100xxxxxxxxxx  # Channel ID for premium purchase logs
```

### 4. Get Required Credentials

#### Telegram Bot Token:
1. Message [@BotFather](https://t.me/BotFather) on Telegram
2. Send `/newbot`
3. Follow the prompts
4. Copy the bot token

#### API ID & API Hash:
1. Visit [my.telegram.org](https://my.telegram.org)
2. Login with your phone number
3. Go to "API Development Tools"
4. Create a new application
5. Copy API ID and API Hash

#### MongoDB Database:
1. Create account on [MongoDB Atlas](https://www.mongodb.com/cloud/atlas)
2. Create a free cluster
3. Create a database user
4. Get connection string (replace password and database name)

#### Bin Channel & Premium Logs:
1. Create two private channels
2. Add your bot as admin to both channels
3. Get channel ID using [@RawDataBot](https://t.me/RawDataBot)
   - Forward any message from the channel to this bot
   - Copy the `chat.id` value (will be negative number like -1001234567890)

### 5. Run the Bot

```bash
python bot.py
```

## 📚 Commands

### 👤 User Commands
- `/start` - Start the bot
- `/help` - Show help message
- `/myplan` - Check your premium subscription
- `/addthum` - Add custom thumbnail (Premium only)
- `/viewthum` - View your current thumbnail
- `/delthum` - Delete your thumbnail
- `/settings` - Configure upload settings

### 👨‍💼 Admin Commands
- `/broadcast` - Broadcast message to all users
- `/grp_broadcast` - Broadcast message to all groups
- `/add_premium` - Add premium to user
  - Usage: `/add_premium user_id 1 month`
  - Formats: `1 day`, `1 hour`, `1 min`, `1 month`, `1 year`
- `/remove_premium` - Remove premium from user
  - Usage: `/remove_premium user_id`
- `/get_premium` - Get premium info of a user
  - Usage: `/get_premium user_id`
- `/premium_users` - List all premium users
- `/banned` - List all banned users
- `/clear_junk` - Remove blocked/deleted users from database
- `/clear_junk_group` - Remove inaccessible groups from database

## 💳 Premium Plans

The bot supports Telegram Star payments with the following plans:

| Duration | Price |
|----------|-------|
| 1 Month  | 50⭐  |
| 3 Months | 100⭐ |
| 6 Months | 200⭐ |
| 1 Year   | 350⭐ |

## 🔧 Configuration Files

### `config.py`
Main configuration file containing all bot settings:
- Bot credentials
- Database settings
- Admin configuration
- Premium plans
- Force subscribe channels
- AdFly API settings
- File size limits
- Link expiry settings

### `script.py`
Contains all bot messages and text templates. Edit this file to customize bot messages.

### `utils.py`
Utility functions for the bot:
- Time formatting
- File size formatting
- URL shortening with AdFly
- Greeting based on timezone
- Broadcast functions

## 📁 Project Structure

```
telegram_file_link_bot/
├── bot.py                  # Main bot file
├── config.py               # Configuration
├── script.py               # Bot messages
├── utils.py                # Utility functions
├── requirements.txt        # Dependencies
├── .env.example            # Environment template
├── database/
│   └── users_chats_db.py   # Database operations
└── plugins/
    ├── start.py            # Start command & force subscribe
    ├── file_handler.py     # File upload & link generation
    ├── premium.py          # Premium features & Star payments
    ├── settings.py         # User settings & thumbnails
    ├── broadcast.py        # Broadcast commands
    └── ban.py              # Ban management
```

## 🌟 Features Explained

### Force Subscribe
Users must join configured channels before using the bot:
- `@zerodev2`
- `@mvxyoffcail`

Channels can be changed in `config.py`.

### Random Anime Wallpapers
Welcome messages include random anime wallpapers from:
`https://api.aniwallpaper.workers.dev/random?type=girl`

### AdFly Integration
All links are automatically shortened using AdFly API for monetization.

### Greeting System
Bot shows time-based greetings for India/Sri Lanka timezone:
- 🌅 Good Morning (5 AM - 12 PM)
- ☀️ Good Afternoon (12 PM - 5 PM)
- 🌆 Good Evening (5 PM - 9 PM)
- 🌙 Good Night (9 PM - 5 AM)

### Animated Start
When user starts the bot:
1. ⏳ Hourglass emoji appears for 2 seconds
2. Auto-deletes
3. Welcome message with random anime wallpaper appears

## 🚀 Deployment

### Heroku
1. Create new app on Heroku
2. Connect to GitHub repository
3. Add Config Vars (same as .env file)
4. Deploy

### VPS
1. Install Python 3.9+
2. Clone repository
3. Install dependencies
4. Configure .env
5. Run with screen or systemd:

```bash
# Using screen
screen -S filebot
python bot.py

# Using systemd (create service file)
sudo systemctl enable filebot
sudo systemctl start filebot
```

## 📝 Important Notes

1. **Bin Channel**: Must be a private channel where bot is admin
2. **Premium Logs**: Separate channel for premium purchase logging
3. **File Storage**: Files are stored in Telegram's bin channel
4. **Database**: MongoDB stores user data, file metadata, and settings
5. **AdFly API**: Pre-configured with provided API key

## 🆘 Support

- **Developer**: [@Venuboyy](https://t.me/Venuboyy)
- **Channel 1**: [@zerodev2](https://t.me/zerodev2)
- **Channel 2**: [@mvxyoffcail](https://t.me/mvxyoffcail)

## ⚖️ License

This project is for educational purposes. Please comply with Telegram's Terms of Service.

## 🙏 Credits

- **Developer**: Zerodev
- **Pyrogram**: Telegram MTProto API framework
- **MongoDB**: Database
- **AdFly**: Link monetization

---

Made with ❤️ by Zerodev
