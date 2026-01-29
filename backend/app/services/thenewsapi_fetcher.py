import logging
import hashlib
from datetime import datetime, date

import httpx

from app.config import settings

logger = logging.getLogger(__name__)

THENEWSAPI_BASE_URL = "https://api.thenewsapi.com/v1/news/top"

# Track daily usage (resets each day)
_usage_tracker = {
    "date": None,
    "requests": 0,
}
MAX_DAILY_REQUESTS = 3


def _check_rate_limit() -> bool:
    """Check if we're within the daily rate limit."""
    today = date.today()
    if _usage_tracker["date"] != today:
        _usage_tracker["date"] = today
        _usage_tracker["requests"] = 0

    return _usage_tracker["requests"] < MAX_DAILY_REQUESTS


def _increment_usage():
    """Increment the daily usage counter."""
    _usage_tracker["requests"] += 1
    remaining = MAX_DAILY_REQUESTS - _usage_tracker["requests"]
    logger.info(f"TheNewsAPI usage: {_usage_tracker['requests']}/{MAX_DAILY_REQUESTS} today ({remaining} remaining)")


def get_thenewsapi_usage() -> dict:
    """Get current TheNewsAPI usage stats."""
    today = date.today()
    if _usage_tracker["date"] != today:
        return {"requests": 0, "limit": MAX_DAILY_REQUESTS, "remaining": MAX_DAILY_REQUESTS}

    remaining = MAX_DAILY_REQUESTS - _usage_tracker["requests"]
    return {
        "requests": _usage_tracker["requests"],
        "limit": MAX_DAILY_REQUESTS,
        "remaining": remaining,
    }


def parse_thenewsapi_date(date_str: str | None) -> datetime | None:
    """Parse TheNewsAPI date format."""
    if not date_str:
        return None
    try:
        return datetime.fromisoformat(date_str.replace("Z", "+00:00"))
    except (ValueError, TypeError):
        return None


def generate_guid(url: str) -> str:
    """Generate a unique ID from URL if uuid not provided."""
    return hashlib.md5(url.encode()).hexdigest()


async def fetch_thenewsapi_articles() -> list[dict]:
    """Fetch articles from The News API."""
    if not settings.THENEWSAPI_ENABLED:
        logger.debug("TheNewsAPI is disabled")
        return []

    if not settings.THENEWSAPI_KEY:
        logger.warning("TheNewsAPI key not configured")
        return []

    if not _check_rate_limit():
        logger.info("TheNewsAPI daily limit reached (3 requests/day), skipping")
        return []

    logger.info("Fetching articles from TheNewsAPI")

    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.get(
                THENEWSAPI_BASE_URL,
                params={
                    "api_token": settings.THENEWSAPI_KEY,
                    "language": "en",
                    "limit": 100,
                },
            )
            response.raise_for_status()
            _increment_usage()

            data = response.json()
            articles = []

            for item in data.get("data", []):
                guid = item.get("uuid") or generate_guid(item.get("url", ""))
                articles.append({
                    "guid": guid,
                    "title": item.get("title", ""),
                    "summary": item.get("description", ""),
                    "link": item.get("url", ""),
                    "source_name": item.get("source", "TheNewsAPI"),
                    "image_url": item.get("image_url"),
                    "published": parse_thenewsapi_date(item.get("published_at")),
                })

            logger.info(f"TheNewsAPI: fetched {len(articles)} articles")
            return articles

    except httpx.HTTPStatusError as e:
        logger.error(f"TheNewsAPI error: {e.response.status_code}")
        return []
    except Exception as e:
        logger.error(f"TheNewsAPI fetch failed: {e}")
        return []
