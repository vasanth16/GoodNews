import re
import feedparser
import httpx
from datetime import datetime
from time import struct_time

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Article
from app.services.content_filter import (
    calculate_hopefulness_score,
    detect_category,
    should_include,
)


RSS_SOURCES = [
    {"name": "Positive News", "url": "https://www.positive.news/feed/"},
    {"name": "Good News Network", "url": "https://www.goodnewsnetwork.org/feed/"},
    {"name": "Reasons to be Cheerful", "url": "https://reasonstobecheerful.world/feed/"},
]


def parse_published_date(date_parsed: struct_time | None) -> datetime | None:
    """Convert feedparser's time tuple to datetime."""
    if date_parsed is None:
        return None
    try:
        return datetime(*date_parsed[:6])
    except (TypeError, ValueError):
        return None


def extract_image_url(entry: dict) -> str | None:
    """Extract image URL from RSS entry using various methods."""
    # Try media:content
    if hasattr(entry, "media_content") and entry.media_content:
        for media in entry.media_content:
            if media.get("medium") == "image" or media.get("type", "").startswith("image/"):
                return media.get("url")
        # If no explicit image type, take first media_content with url
        if entry.media_content[0].get("url"):
            return entry.media_content[0].get("url")

    # Try media:thumbnail
    if hasattr(entry, "media_thumbnail") and entry.media_thumbnail:
        return entry.media_thumbnail[0].get("url")

    # Try enclosures
    if hasattr(entry, "enclosures") and entry.enclosures:
        for enclosure in entry.enclosures:
            if enclosure.get("type", "").startswith("image/"):
                return enclosure.get("href") or enclosure.get("url")

    # Try links with image type
    if hasattr(entry, "links"):
        for link in entry.links:
            if link.get("type", "").startswith("image/"):
                return link.get("href")

    return None


async def fetch_og_image(url: str) -> str | None:
    """Fetch og:image meta tag from article URL."""
    try:
        async with httpx.AsyncClient(timeout=10.0, follow_redirects=True) as client:
            response = await client.get(url, headers={
                "User-Agent": "Mozilla/5.0 (compatible; BrightWorldNews/1.0)"
            })
            if response.status_code != 200:
                return None

            html = response.text[:50000]  # Only check first 50KB

            # Look for og:image meta tag
            patterns = [
                r'<meta[^>]+property=["\']og:image["\'][^>]+content=["\']([^"\']+)["\']',
                r'<meta[^>]+content=["\']([^"\']+)["\'][^>]+property=["\']og:image["\']',
            ]

            for pattern in patterns:
                match = re.search(pattern, html, re.IGNORECASE)
                if match:
                    return match.group(1)

            return None
    except Exception:
        return None


def fetch_rss_feed(url: str) -> list[dict]:
    """Fetch and parse an RSS feed, returning a list of article dicts."""
    try:
        feed = feedparser.parse(url)
        articles = []

        for entry in feed.entries:
            article = {
                "title": entry.get("title", ""),
                "link": entry.get("link", ""),
                "summary": entry.get("summary") or entry.get("description", ""),
                "published": parse_published_date(entry.get("published_parsed")),
                "guid": entry.get("id") or entry.get("link", ""),
                "image_url": extract_image_url(entry),
            }
            articles.append(article)

        return articles
    except Exception:
        return []


def fetch_all_sources() -> list[dict]:
    """Fetch articles from all RSS sources."""
    all_articles = []

    for source in RSS_SOURCES:
        articles = fetch_rss_feed(source["url"])
        for article in articles:
            article["source_name"] = source["name"]
        all_articles.extend(articles)

    return all_articles


async def store_articles(articles: list[dict], session: AsyncSession) -> int:
    """Store articles in the database, skipping duplicates and filtered content."""
    new_count = 0

    for article_data in articles:
        guid = article_data.get("guid")
        if not guid:
            continue

        headline = article_data.get("title", "")
        summary = article_data.get("summary") or ""

        # Skip articles with too many negative keywords
        if not should_include(headline, summary):
            continue

        result = await session.execute(select(Article).where(Article.guid == guid))
        existing = result.scalar_one_or_none()

        if existing:
            continue

        # Calculate hopefulness score and category
        hopefulness_score = calculate_hopefulness_score(headline, summary)
        category = detect_category(headline, summary)

        # Get image URL - try RSS first, then fetch og:image from page
        image_url = article_data.get("image_url")
        if not image_url:
            article_link = article_data.get("link", "")
            if article_link:
                image_url = await fetch_og_image(article_link)

        article = Article(
            guid=guid,
            headline=headline,
            summary=summary,
            source_url=article_data.get("link", ""),
            source_name=article_data.get("source_name", ""),
            image_url=image_url,
            published_at=article_data.get("published"),
            hopefulness_score=hopefulness_score,
            category=category,
        )
        session.add(article)
        new_count += 1

    await session.commit()
    return new_count


async def fetch_and_store(session: AsyncSession) -> dict:
    """Fetch all RSS sources and store new articles in the database."""
    articles = fetch_all_sources()
    new_count = await store_articles(articles, session)

    return {"fetched": len(articles), "new": new_count}
