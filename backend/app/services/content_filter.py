POSITIVE_KEYWORDS = {
    "high": [
        "breakthrough",
        "cure",
        "solution",
        "success",
        "achievement",
        "milestone",
        "progress",
        "innovation",
        "record-breaking",
    ],
    "medium": [
        "improve",
        "growth",
        "recover",
        "restore",
        "support",
        "community",
        "volunteer",
        "protect",
        "save",
        "launch",
    ],
    "low": ["new", "first", "discover", "develop", "create", "announce"],
}

NEGATIVE_KEYWORDS = [
    "death",
    "killed",
    "murder",
    "war",
    "attack",
    "crisis",
    "disaster",
    "tragedy",
    "victim",
    "shooting",
    "terrorist",
    "crash",
    "scandal",
    "rape",
    "assault",
]

CATEGORY_KEYWORDS = {
    "environment": [
        "climate",
        "renewable",
        "solar",
        "wind",
        "conservation",
        "species",
        "ocean",
        "forest",
        "sustainable",
        "emissions",
    ],
    "health": [
        "cure",
        "treatment",
        "vaccine",
        "medical",
        "disease",
        "mental health",
        "therapy",
        "hospital",
        "cancer",
    ],
    "technology": [
        "ai",
        "robot",
        "software",
        "app",
        "digital",
        "innovation",
        "startup",
        "tech",
        "computer",
    ],
    "social": [
        "community",
        "education",
        "equality",
        "rights",
        "justice",
        "volunteer",
        "nonprofit",
        "charity",
    ],
    "humanitarian": [
        "refugee",
        "aid",
        "rescue",
        "poverty",
        "hunger",
        "shelter",
        "donation",
        "relief",
    ],
}


def calculate_hopefulness_score(headline: str, summary: str) -> float:
    """Calculate a hopefulness score based on positive and negative keywords."""
    text = f"{headline} {summary}".lower()
    score = 0.0

    # Add points for positive keywords
    for keyword in POSITIVE_KEYWORDS["high"]:
        if keyword in text:
            score += 0.25
    for keyword in POSITIVE_KEYWORDS["medium"]:
        if keyword in text:
            score += 0.12
    for keyword in POSITIVE_KEYWORDS["low"]:
        if keyword in text:
            score += 0.05

    # Subtract points for negative keywords
    for keyword in NEGATIVE_KEYWORDS:
        if keyword in text:
            score -= 0.3

    # Clamp between 0.0 and 1.0
    return max(0.0, min(1.0, score))


def detect_category(headline: str, summary: str) -> str:
    """Detect the category based on keyword matches."""
    text = f"{headline} {summary}".lower()
    category_counts: dict[str, int] = {}

    for category, keywords in CATEGORY_KEYWORDS.items():
        count = sum(1 for keyword in keywords if keyword in text)
        if count > 0:
            category_counts[category] = count

    if not category_counts:
        return "general"

    return max(category_counts, key=lambda k: category_counts[k])


def should_include(headline: str, summary: str) -> bool:
    """Determine if an article should be included based on negative keyword count."""
    text = f"{headline} {summary}".lower()
    negative_count = sum(1 for keyword in NEGATIVE_KEYWORDS if keyword in text)
    return negative_count < 2
