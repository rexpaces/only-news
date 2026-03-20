import re
import time
import logging
from datetime import datetime, timezone

import feedparser
from dotenv import load_dotenv

from feeds import CATEGORY_FEEDS, REGION_FEEDS
from ollama_client import process_article
import local_db
import remote_db

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
)
logger = logging.getLogger(__name__)

HTML_TAG_RE = re.compile(r"<[^>]+>")
ITEMS_PER_CATEGORY_FEED = 20
ITEMS_PER_REGION_FEED = 10
OLLAMA_DELAY = 0.3


def strip_html(text: str) -> str:
    return HTML_TAG_RE.sub("", text).strip()


def parse_date(entry) -> str:
    for attr in ("published_parsed", "updated_parsed"):
        val = getattr(entry, attr, None)
        if val:
            try:
                return datetime(*val[:6], tzinfo=timezone.utc).isoformat()
            except Exception:
                pass
    return datetime.now(timezone.utc).isoformat()


def process_feed_entry(entry, region: str, source: str) -> bool:
    url = entry.get("link", "")
    if not url:
        return False

    if local_db.url_exists(url):
        return False

    title = entry.get("title", "").strip()
    if not title:
        return False

    raw_desc = entry.get("summary", "") or entry.get("description", "")
    description = strip_html(raw_desc)

    logger.info(f"  Processing: {title[:70]}...")
    processed = process_article(title, description)

    local_db.insert_article({
        "title": processed["title"],
        "description": processed["description"],
        "original_title": title,
        "url": url,
        "category": processed["category"],
        "region": region,
        "source": source,
        "published_at": parse_date(entry),
    })
    time.sleep(OLLAMA_DELAY)
    return True


def collect_all_feeds():
    logger.info("=== Collecting category feeds ===")
    for category, urls in CATEGORY_FEEDS.items():
        for feed_url in urls:
            logger.info(f"Fetching [{category}] {feed_url}")
            try:
                feed = feedparser.parse(feed_url)
                source = feed.feed.get("title", feed_url)
                count = 0
                for entry in feed.entries[:ITEMS_PER_CATEGORY_FEED]:
                    if process_feed_entry(entry, "Global", source):
                        count += 1
                logger.info(f"  Inserted {count} new articles locally")
            except Exception as e:
                logger.error(f"Error processing feed {feed_url}: {e}")

    logger.info("=== Collecting region feeds ===")
    for city, feed_url in REGION_FEEDS.items():
        logger.info(f"Fetching [{city}]")
        try:
            feed = feedparser.parse(feed_url)
            count = 0
            for entry in feed.entries[:ITEMS_PER_REGION_FEED]:
                source = "Google News"
                if hasattr(entry, "source") and isinstance(entry.source, dict):
                    source = entry.source.get("title", "Google News")
                if process_feed_entry(entry, city, source):
                    count += 1
            logger.info(f"  Inserted {count} new articles locally")
        except Exception as e:
            logger.error(f"Error processing region {city}: {e}")


def sync_to_remote():
    logger.info("=== Syncing to remote MongoDB ===")
    unsynced = local_db.get_unsynced()
    if not unsynced:
        logger.info("Nothing to sync.")
        return
    logger.info(f"Syncing {len(unsynced)} articles to remote...")
    inserted = remote_db.bulk_insert(unsynced)
    local_db.mark_synced([a["_id"] for a in unsynced])
    logger.info(f"Done — {inserted} new articles pushed to remote.")


if __name__ == "__main__":
    load_dotenv()

    local_db.ensure_indexes()
    remote_db.ensure_indexes()

    logger.info("Starting only-news collector...")
    collect_all_feeds()
    sync_to_remote()
    logger.info("All done.")
