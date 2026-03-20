import os
import logging

from pymongo import MongoClient as PyMongoClient
from pymongo.server_api import ServerApi
from pymongo.errors import BulkWriteError

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


def bulk_insert(articles: list) -> int:
    if not articles:
        return 0
    docs = [{k: v for k, v in a.items() if k not in ("_id", "synced")} for a in articles]
    try:
        result = get_collection().insert_many(docs, ordered=False)
        return len(result.inserted_ids)
    except BulkWriteError as e:
        inserted = e.details.get("nInserted", 0)
        logger.warning(f"Bulk write: {inserted} inserted, some duplicates skipped")
        return inserted
