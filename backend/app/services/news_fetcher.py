import feedparser
from datetime import datetime
from time import struct_time

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Article


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
    """Store articles in the database, skipping duplicates by guid."""
    new_count = 0

    for article_data in articles:
        guid = article_data.get("guid")
        if not guid:
            continue

        result = await session.execute(select(Article).where(Article.guid == guid))
        existing = result.scalar_one_or_none()

        if existing:
            continue

        article = Article(
            guid=guid,
            headline=article_data.get("title", ""),
            summary=article_data.get("summary"),
            source_url=article_data.get("link", ""),
            source_name=article_data.get("source_name", ""),
            image_url=article_data.get("image_url"),
            published_at=article_data.get("published"),
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
