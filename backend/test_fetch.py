import asyncio
from app.database import async_session, init_db
from app.services.news_fetcher import fetch_and_store


async def main():
    print("Initializing database...")
    await init_db()

    print("Fetching and storing articles...\n")

    async with async_session() as session:
        result = await fetch_and_store(session)

    print(f"Total articles fetched: {result['fetched']}")
    print(f"New articles stored: {result['new']}")


if __name__ == "__main__":
    asyncio.run(main())
