from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_session
from app.models import Article
from app.schemas import ArticleResponse, ArticleListResponse
from app.services.news_fetcher import fetch_and_store

router = APIRouter(prefix="/articles", tags=["articles"])


@router.get("", response_model=ArticleListResponse)
async def get_articles(
    limit: int = Query(default=20, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    session: AsyncSession = Depends(get_session),
):
    """Fetch paginated articles ordered by published date."""
    # Get total count
    count_result = await session.execute(select(func.count(Article.id)))
    total = count_result.scalar_one()

    # Get articles
    query = (
        select(Article)
        .order_by(Article.published_at.desc())
        .offset(offset)
        .limit(limit)
    )
    result = await session.execute(query)
    articles = result.scalars().all()

    return ArticleListResponse(
        articles=articles,
        total=total,
        limit=limit,
        offset=offset,
        has_more=offset + len(articles) < total,
    )


@router.post("/fetch")
async def trigger_fetch(session: AsyncSession = Depends(get_session)):
    """Trigger fetching articles from all RSS sources."""
    result = await fetch_and_store(session)
    return {"status": "ok", "fetched": result["fetched"], "new": result["new"]}


@router.get("/{article_id}", response_model=ArticleResponse)
async def get_article(
    article_id: int,
    session: AsyncSession = Depends(get_session),
):
    """Fetch a single article by ID."""
    result = await session.execute(select(Article).where(Article.id == article_id))
    article = result.scalar_one_or_none()

    if article is None:
        raise HTTPException(status_code=404, detail="Article not found")

    return article
