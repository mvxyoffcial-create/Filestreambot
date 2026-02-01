import os
import re
from os import environ
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Text Patterns (must be defined before use)
id_pattern = re.compile(r'^.\d+$')

# Bot Configuration
BOT_TOKEN = environ.get("BOT_TOKEN", "")
API_ID = int(environ.get("API_ID", "12345"))
API_HASH = environ.get("API_HASH", "")

# Database
DATABASE_URI = environ.get("DATABASE_URI", "")
DATABASE_NAME = environ.get("DATABASE_NAME", "FileToLink")

# Admin & Channel Settings
ADMINS = [int(admin) if id_pattern.search(admin) else admin for admin in environ.get('ADMINS', '').split()]
BIN_CHANNEL = int(environ.get("BIN_CHANNEL", "-100"))
SUPPORT_CHAT = environ.get("SUPPORT_CHAT", "https://t.me/zerodev2")
OWNER = environ.get("OWNER", "@Venuboyy")

# Base URL for file links
BASE_URL = environ.get("BASE_URL", "https://filetolinkbot-97hf.onrender.com")

# Force Subscribe Channels
FORCE_SUB_CHANNELS = [
    "zerodev2",
    "mvxyoffcail"
]

# AdFly API Configuration
ADFLY_API_KEY = "9a4803974a9dc9c639002d42c5a67f7c18961c0e"
ADFLY_API_URL = "https://adfly.site/api"

# Premium Configuration
PREMIUM_LOGS = int(environ.get("PREMIUM_LOGS", "-100"))

# Star Payment Plans (amount: duration)
STAR_PREMIUM_PLANS = {
    50: "1 month",
    100: "3 months",
    200: "6 months",
    350: "1 year"
}

# Images
SUBSCRIPTION = "https://i.ibb.co/pr2H8cwT/img-8312532076.jpg"
FORCE_SUB_IMAGE = "https://i.ibb.co/pr2H8cwT/img-8312532076.jpg"
RANDOM_ANIME_API = "https://api.aniwallpaper.workers.dev/random?type=girl"

# File Settings
MAX_FILE_SIZE = 4 * 1024 * 1024 * 1024  # 4GB in bytes
FREE_USER_LIMIT = 4 * 1024 * 1024 * 1024  # 4GB for free users

# Link Expiry
FREE_USER_LINK_EXPIRY = 24 * 60 * 60  # 24 hours in seconds
PREMIUM_USER_LINK_EXPIRY = None  # Permanent for premium users

# Download Speed Limits (bytes per second)
FREE_USER_SPEED_LIMIT = 512 * 1024  # 512 KB/s
PREMIUM_USER_SPEED_LIMIT = None  # Unlimited
