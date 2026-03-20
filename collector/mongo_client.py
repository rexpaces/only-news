import os
import hashlib
import logging
from datetime import datetime, timezone

from pymongo import MongoClient as PyMongoClient
from pymongo.server_api import ServerApi
from pymongo.errors import DuplicateKeyError

logger = logging.getLogger(__name__)

_client = None


def get_collection():
    global _client
    if _client is None:
        uri = os.environ["MONGODB_URI"]
        _client = PyMongoClient(uri, server_api=ServerApi("1"))
    db_name = os.environ.get("MONGODB_DATABASE", "only_news")
    return _client[db_name]["news"]


def ensure_indexes():
    col = get_collection()
    col.create_index("url_hash", unique=True)
    col.create_index([("published_at", -1)])
    col.create_index("category")


def url_exists(url: str) -> bool:
    url_hash = hashlib.md5(url.encode()).hexdigest()
    return get_collection().find_one({"url_hash": url_hash}, {"_id": 1}) is not None


def insert_article(article: dict) -> bool:
    url_hash = hashlib.md5(article["url"].encode()).hexdigest()
    doc = {
        **article,
        "url_hash": url_hash,
        "collected_at": datetime.now(timezone.utc).isoformat(),
    }
    try:
        get_collection().insert_one(doc)
        return True
    except DuplicateKeyError:
        return False
