import datetime
import motor.motor_asyncio
from config import DATABASE_URI, DATABASE_NAME

class Database:
    def __init__(self, uri, database_name):
        self._client = motor.motor_asyncio.AsyncIOMotorClient(uri)
        self.db = self._client[database_name]
        self.col = self.db.users
        self.grp = self.db.groups
        self.files = self.db.files
        self.banned = self.db.banned_users
        self.banned_chats = self.db.banned_chats

    # User Management
    def new_user(self, id):
        return dict(
            id=id,
            join_date=datetime.date.today().isoformat(),
            ban_status=dict(
                is_banned=False,
                ban_reason="",
            ),
            expiry_time=None,
            thumbnail=None,
            upload_mode="document"  # document or video
        )

    async def add_user(self, id):
        user = self.new_user(id)
        await self.col.insert_one(user)

    async def is_user_exist(self, id):
        user = await self.col.find_one({'id': int(id)})
        return bool(user)

    async def total_users_count(self):
        count = await self.col.count_documents({})
        return count

    async def get_all_users(self):
        all_users = self.col.find({})
        return all_users

    async def delete_user(self, user_id):
        await self.col.delete_many({'id': int(user_id)})

    async def remove_ban(self, id):
        ban_status = dict(
            is_banned=False,
            ban_reason='',
        )
        await self.col.update_one({'id': id}, {'$set': {'ban_status': ban_status}})

    async def ban_user(self, user_id, ban_reason="No Reason"):
        ban_status = dict(
            is_banned=True,
            ban_reason=ban_reason,
        )
        await self.col.update_one({'id': user_id}, {'$set': {'ban_status': ban_status}})

    async def get_ban_status(self, id):
        default = dict(
            is_banned=False,
            ban_reason='',
        )
        user = await self.col.find_one({'id': int(id)})
        return user.get('ban_status', default) if user else default

    async def get_all_banned_users(self):
        banned_users = self.col.find({'ban_status.is_banned': True})
        return banned_users

    async def get_banned(self):
        users = self.col.find({'ban_status.is_banned': True})
        chats = self.grp.find({'chat_status.is_disabled': True})
        b_chats = [chat['id'] async for chat in chats]
        b_users = [user['id'] async for user in users]
        return b_users, b_chats

    # Premium Management
    async def update_user(self, user_data):
        await self.col.update_one({'id': user_data['id']}, {'$set': user_data}, upsert=True)

    async def get_user(self, user_id):
        user = await self.col.find_one({'id': int(user_id)})
        return user

    async def remove_premium_access(self, user_id):
        user = await self.col.find_one({'id': int(user_id)})
        if user and user.get('expiry_time'):
            await self.col.update_one({'id': int(user_id)}, {'$set': {'expiry_time': None}})
            return True
        return False

    async def check_premium(self, user_id):
        """Check if user has active premium"""
        user = await self.col.find_one({'id': int(user_id)})
        if user and user.get('expiry_time'):
            if user['expiry_time'] > datetime.datetime.now():
                return True
            else:
                # Premium expired, remove it
                await self.col.update_one({'id': int(user_id)}, {'$set': {'expiry_time': None}})
        return False

    # Thumbnail Management
    async def set_thumbnail(self, user_id, file_id):
        await self.col.update_one({'id': int(user_id)}, {'$set': {'thumbnail': file_id}}, upsert=True)

    async def get_thumbnail(self, user_id):
        user = await self.col.find_one({'id': int(user_id)})
        return user.get('thumbnail') if user else None

    async def delete_thumbnail(self, user_id):
        await self.col.update_one({'id': int(user_id)}, {'$set': {'thumbnail': None}})

    # Upload Mode Settings
    async def set_upload_mode(self, user_id, mode):
        await self.col.update_one({'id': int(user_id)}, {'$set': {'upload_mode': mode}}, upsert=True)

    async def get_upload_mode(self, user_id):
        user = await self.col.find_one({'id': int(user_id)})
        return user.get('upload_mode', 'document') if user else 'document'

    # Group Management
    def new_group(self, id):
        return dict(
            id=id,
            chat_status=dict(
                is_disabled=False,
                reason="",
            ),
        )

    async def add_chat(self, chat_id):
        chat = self.new_group(chat_id)
        await self.grp.insert_one(chat)

    async def get_chat(self, chat_id):
        chat = await self.grp.find_one({'id': int(chat_id)})
        return chat if chat else self.new_group(chat_id)

    async def is_chat_exist(self, chat_id):
        chat = await self.grp.find_one({'id': int(chat_id)})
        return bool(chat)

    async def total_chat_count(self):
        count = await self.grp.count_documents({})
        return count

    async def get_all_chats(self):
        all_chats = self.grp.find({})
        return all_chats

    async def delete_chat(self, chat_id):
        await self.grp.delete_many({'id': int(chat_id)})

    async def disable_chat(self, chat_id, reason="No Reason"):
        chat_status = dict(
            is_disabled=True,
            reason=reason,
        )
        await self.grp.update_one({'id': int(chat_id)}, {'$set': {'chat_status': chat_status}})

    async def enable_chat(self, chat_id):
        chat_status = dict(
            is_disabled=False,
            reason="",
        )
        await self.grp.update_one({'id': int(chat_id)}, {'$set': {'chat_status': chat_status}})

    # File Storage Management
    async def save_file(self, file_data):
        """Save file information to database"""
        await self.files.insert_one(file_data)
        return str(file_data['_id'])

    async def get_file(self, file_id):
        """Get file information from database"""
        from bson.objectid import ObjectId
        try:
            file_data = await self.files.find_one({'_id': ObjectId(file_id)})
            return file_data
        except:
            return None

    async def delete_file(self, file_id):
        """Delete file from database"""
        from bson.objectid import ObjectId
        try:
            await self.files.delete_one({'_id': ObjectId(file_id)})
            return True
        except:
            return False

    async def update_file_links(self, file_id, stream_link, download_link):
        """Update file with generated links"""
        from bson.objectid import ObjectId
        try:
            await self.files.update_one(
                {'_id': ObjectId(file_id)},
                {'$set': {
                    'stream_link': stream_link,
                    'download_link': download_link,
                    'created_at': datetime.datetime.now()
                }}
            )
            return True
        except:
            return False

    async def check_file_expiry(self, file_id):
        """Check if file link has expired"""
        file_data = await self.get_file(file_id)
        if not file_data:
            return True
        
        # If user is premium, links don't expire
        if file_data.get('is_premium'):
            return False
        
        # For free users, check 24 hour expiry
        created_at = file_data.get('created_at')
        if created_at:
            expiry_time = created_at + datetime.timedelta(hours=24)
            if datetime.datetime.now() > expiry_time:
                return True
        
        return False

db = Database(DATABASE_URI, DATABASE_NAME)
