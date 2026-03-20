import os
import hashlib
import logging
from datetime import datetime, timezone

from pymongo import MongoClient as PyMongoClient
from pymongo.errors import DuplicateKeyError

logger = logging.getLogger(__name__)

_client = None


def get_collection():
    global _client
    if _client is None:
        uri = os.environ.get("MONGODB_URI_LOCAL", "mongodb://localhost:27017")
        _client = PyMongoClient(uri)
    db_name = os.environ.get("MONGODB_DATABASE", "only_news") + "_local"
    return _client[db_name]["news"]


def ensure_indexes():
    col = get_collection()
    col.create_index("url_hash", unique=True)
    col.create_index("synced")
    col.create_index([("published_at", -1)])


def url_exists(url: str) -> bool:
    url_hash = hashlib.md5(url.encode()).hexdigest()
    return get_collection().find_one({"url_hash": url_hash}, {"_id": 1}) is not None


def insert_article(article: dict) -> bool:
    url_hash = hashlib.md5(article["url"].encode()).hexdigest()
    try:
        get_collection().insert_one({
            **article,
            "url_hash": url_hash,
            "synced": False,
            "collected_at": datetime.now(timezone.utc).isoformat(),
        })
        return True
    except DuplicateKeyError:
        return False


def get_unsynced() -> list:
    return list(get_collection().find({"synced": False}))


def mark_synced(ids: list) -> None:
    get_collection().update_many(
        {"_id": {"$in": ids}},
        {"$set": {"synced": True}},
    )
