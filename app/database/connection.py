from pymongo import MongoClient, errors
from app.config.settings import settings
from typing import Any

client = MongoClient(settings.MONGO_URI, serverSelectionTimeoutMS=5000)

def get_master_db() -> Any:
    
    """
    Returns a reference to the master database used for metadata,
    admin credentials and collection registration.
    """
    return client[settings.MASTER_DB_NAME]

try:
    client.server_info()
except errors.ServerSelectionTimeoutError:
    pass
