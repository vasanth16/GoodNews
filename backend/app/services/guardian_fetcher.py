import logging
from datetime import datetime, date

import httpx

from app.config import settings

logger = logging.getLogger(__name__)

GUARDIAN_BASE_URL = "https://content.guardianapis.com"
GUARDIAN_SECTIONS = [
    "world",
    "environment",
    "science",
    "global-development",
    "society",
    "technology",
]

# Track daily usage (resets each day)
_usage_tracker = {
    "date": None,
    "requests": 0,
}
MAX_DAILY_REQUESTS = 500
WARNING_THRESHOLD = 400  # Warn when approaching limit


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

    if _usage_tracker["requests"] >= WARNING_THRESHOLD:
        remaining = MAX_DAILY_REQUESTS - _usage_tracker["requests"]
        logger.warning(f"Guardian API approaching limit: {_usage_tracker['requests']}/{MAX_DAILY_REQUESTS} ({remaining} remaining)")
    else:
        logger.debug(f"Guardian API usage: {_usage_tracker['requests']}/{MAX_DAILY_REQUESTS} today")


def get_guardian_usage() -> dict:
    """Get current Guardian API usage stats."""
    today = date.today()
    if _usage_tracker["date"] != today:
        return {"requests": 0, "limit": MAX_DAILY_REQUESTS, "remaining": MAX_DAILY_REQUESTS}

    remaining = MAX_DAILY_REQUESTS - _usage_tracker["requests"]
    return {
        "requests": _usage_tracker["requests"],
        "limit": MAX_DAILY_REQUESTS,
        "remaining": remaining,
    }


def parse_guardian_date(date_str: str | None) -> datetime | None:
    """Parse Guardian ISO date format."""
    if not date_str:
        return None
    try:
        return datetime.fromisoformat(date_str.replace("Z", "+00:00"))
    except (ValueError, TypeError):
        return None


async def fetch_guardian_section(client: httpx.AsyncClient, section: str) -> list[dict]:
    """Fetch articles from a single Guardian section."""
    # Check rate limit before making request
    if not _check_rate_limit():
        logger.warning(f"Guardian API daily limit reached, skipping section {section}")
        return []

    try:
        response = await client.get(
            f"{GUARDIAN_BASE_URL}/{section}",
            params={
                "api-key": settings.GUARDIAN_API_KEY,
                "show-fields": "headline,standfirst,thumbnail",
                "page-size": 50,
                "order-by": "newest",
            },
        )
        response.raise_for_status()
        _increment_usage()
        data = response.json()

        articles = []
        for item in data.get("response", {}).get("results", []):
            fields = item.get("fields", {})
            articles.append({
                "guid": item.get("id", ""),
                "title": fields.get("headline") or item.get("webTitle", ""),
                "summary": fields.get("standfirst", ""),
                "link": item.get("webUrl", ""),
                "source_name": "The Guardian",
                "image_url": fields.get("thumbnail"),
                "published": parse_guardian_date(item.get("webPublicationDate")),
            })
        return articles

    except httpx.HTTPStatusError as e:
        logger.error(f"Guardian API error for section {section}: {e.response.status_code}")
        return []
    except Exception as e:
        logger.error(f"Guardian fetch failed for section {section}: {e}")
        return []


async def fetch_guardian_articles() -> list[dict]:
    """Fetch articles from all Guardian sections."""
    if not settings.GUARDIAN_ENABLED:
        logger.debug("Guardian API is disabled")
        return []

    if not settings.GUARDIAN_API_KEY:
        logger.warning("Guardian API key not configured")
        return []

    logger.info("Fetching articles from The Guardian API")
    all_articles = []

    async with httpx.AsyncClient(timeout=30.0) as client:
        for section in GUARDIAN_SECTIONS:
            articles = await fetch_guardian_section(client, section)
            all_articles.extend(articles)
            logger.debug(f"Guardian {section}: {len(articles)} articles")

    # Deduplicate by guid (same article can appear in multiple sections)
    seen_guids = set()
    unique_articles = []
    for article in all_articles:
        if article["guid"] not in seen_guids:
            seen_guids.add(article["guid"])
            unique_articles.append(article)

    logger.info(f"Guardian API: fetched {len(unique_articles)} unique articles")
    return unique_articles
