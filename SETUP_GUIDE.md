# 🚀 Quick Setup Guide

## 📝 Step-by-Step Setup

### 1️⃣ Get Telegram Bot Token

1. Open Telegram and search for [@BotFather](https://t.me/BotFather)
2. Send `/newbot`
3. Choose a name for your bot (e.g., "My File Link Bot")
4. Choose a username for your bot (must end with 'bot', e.g., "myfilelink_bot")
5. Copy the **Bot Token** (looks like: `1234567890:ABCdefGHIjklMNOpqrsTUVwxyz`)

### 2️⃣ Get API ID and API Hash

1. Visit [my.telegram.org](https://my.telegram.org)
2. Login with your phone number
3. Click on "API Development Tools"
4. Fill in the application details:
   - App title: Your bot name
   - Short name: anything
   - Platform: Other
   - Description: File to Link Bot
5. Click "Create application"
6. Copy **API ID** and **API Hash**

### 3️⃣ Create MongoDB Database

**Option A: MongoDB Atlas (Free Cloud)**

1. Go to [MongoDB Atlas](https://www.mongodb.com/cloud/atlas/register)
2. Sign up for free account
3. Create a **FREE** cluster (M0 Sandbox)
4. Wait for cluster to be ready (2-5 minutes)
5. Click "Connect" → "Connect your application"
6. Copy the connection string
7. Replace `<password>` with your database password
8. Example: `mongodb+srv://username:password@cluster0.xxxxx.mongodb.net/FileToLink`

**Option B: Local MongoDB**
```bash
# Install MongoDB locally
mongodb://localhost:27017/FileToLink
```

### 4️⃣ Create Bin Channel

1. Create a **private channel** in Telegram
2. Add your bot as **administrator** to this channel
3. Forward any message from the channel to [@RawDataBot](https://t.me/RawDataBot)
4. Copy the `chat.id` (will be negative, like `-1001234567890`)
5. This is your **BIN_CHANNEL**

### 5️⃣ Create Premium Logs Channel

1. Create another **private channel**
2. Add your bot as **administrator**
3. Get the channel ID same way (using @RawDataBot)
4. This is your **PREMIUM_LOGS** channel

### 6️⃣ Get Your User ID

1. Message [@userinfobot](https://t.me/userinfobot)
2. Copy your **User ID** (like `123456789`)
3. This makes you an admin

### 7️⃣ Configure the Bot

1. Rename `.env.example` to `.env`
2. Edit `.env` with your values:

```env
BOT_TOKEN=1234567890:ABCdefGHIjklMNOpqrsTUVwxyz
API_ID=12345678
API_HASH=abcdef1234567890abcdef1234567890
DATABASE_URI=mongodb+srv://username:password@cluster0.xxxxx.mongodb.net/
DATABASE_NAME=FileToLink
ADMINS=123456789 987654321
BIN_CHANNEL=-1001234567890
PREMIUM_LOGS=-1009876543210
```

### 8️⃣ Install and Run

**On Local Computer:**
```bash
# Install Python 3.9 or higher
python --version

# Install dependencies
pip install -r requirements.txt

# Run the bot
python bot.py
```

**Using Startup Script:**
```bash
chmod +x startup.sh
./startup.sh
```

**Using Docker:**
```bash
docker-compose up -d
```

## ✅ Verify Setup

1. Start your bot on Telegram
2. Send `/start` command
3. If you see the welcome message with anime wallpaper → **Setup Successful!** ✅

## 🔧 Common Issues

### Issue: "Module not found"
**Solution:** Install requirements again
```bash
pip install -r requirements.txt --upgrade
```

### Issue: "Invalid bot token"
**Solution:** 
- Check BOT_TOKEN in .env
- Make sure there are no extra spaces
- Get new token from @BotFather if needed

### Issue: "Database connection failed"
**Solution:**
- Check DATABASE_URI
- Make sure password doesn't contain special characters or encode them
- Whitelist your IP in MongoDB Atlas

### Issue: "Force subscribe not working"
**Solution:**
- Make sure channels exist (@zerodev2, @mvxyoffcail)
- Or change channel usernames in `config.py`

## 📱 Testing the Bot

### Test File Upload:
1. Send any file to the bot
2. Should receive stream and download links
3. Links should work

### Test Premium:
1. Use `/add_premium YOUR_USER_ID 1 month`
2. Check with `/myplan`
3. Upload file - should get permanent links

### Test Broadcast:
1. Use `/broadcast` (reply to a message)
2. Choose Yes/No for pinning
3. All users receive the message

## 🎯 Next Steps

1. ✅ Join required channels or update them in config
2. ✅ Test all features
3. ✅ Customize messages in `script.py`
4. ✅ Share your bot with users!

## 💡 Pro Tips

- **Enable Star Payments:** Talk to @BotFather → /mybots → Your Bot → Payments → Connect to Telegram Stars
- **Backup Database:** Export MongoDB data regularly
- **Monitor Logs:** Check console output for errors
- **Update Force Sub:** Edit `config.py` to change required channels

## 🆘 Still Need Help?

Contact Developer: [@Venuboyy](https://t.me/Venuboyy)

---

Made with ❤️ by Zerodev
