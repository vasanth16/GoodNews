from collections import defaultdict
from datetime import datetime


def select_balanced_articles(articles: list[dict], limit: int) -> list[dict]:
    """
    Select articles using round-robin by source for fair distribution.

    Groups articles by source_name, sorts each group by published_at (newest first),
    then picks one from each source in rotation until limit is reached.

    Args:
        articles: List of article dicts with 'source_name' and 'published' keys
        limit: Maximum number of articles to select

    Returns:
        List of selected articles, balanced across sources
    """
    if not articles or limit <= 0:
        return []

    # Group by source
    by_source: dict[str, list[dict]] = defaultdict(list)
    for article in articles:
        source = article.get("source_name", "Unknown")
        by_source[source].append(article)

    # Sort each group by published date (newest first)
    for source in by_source:
        by_source[source].sort(
            key=lambda a: a.get("published") or datetime.min,
            reverse=True
        )

    # Round-robin selection
    selected = []
    source_names = list(by_source.keys())
    source_indices = {source: 0 for source in source_names}

    while len(selected) < limit:
        picked_any = False

        for source in source_names:
            if len(selected) >= limit:
                break

            idx = source_indices[source]
            if idx < len(by_source[source]):
                selected.append(by_source[source][idx])
                source_indices[source] += 1
                picked_any = True

        # If no source had articles left, we're done
        if not picked_any:
            break

    return selected
