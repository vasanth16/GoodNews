import re
from typing import TypedDict

NEGATIVE_KEYWORDS = {
    "violence": [
        "killed", "murder", "shooting", "stabbing", "assault", "robbery",
        "rape", "massacre", "gunman", "homicide", "manslaughter", "arson",
        "kidnap", "terrorist", "terrorism", "bomb", "explosion",
    ],
    "death": [
        "death toll", "dead", "dies", "died", "fatal", "fatality",
        "tragedy", "devastating", "catastrophe", "casualties",
    ],
    "conflict": [
        "slams", "blasts", "rips", "clashes", "controversy", "scandal",
        "impeach", "indicted", "accused", "alleged fraud", "corruption",
    ],
    "negativity": [
        "shocking", "outrage", "fury", "backlash", "sparks anger",
        "horrifying", "gruesome", "horrific", "disturbing",
    ],
}

TRIVIAL_KEYWORDS = {
    "celebrity": [
        "kardashian", "celebrity gossip", "influencer drama", "viral video",
        "tiktok trend", "selfie", "paparazzi", "reality tv",
    ],
    "clickbait": [
        "you won't believe", "shocking reason", "this one trick",
        "gone wrong", "epic fail", "what happens next", "doctors hate",
    ],
}


class FilterResult(TypedDict):
    passed: bool
    reason: str | None


def check_keywords(text: str, keywords: list[str]) -> str | None:
    """Check if text contains any keywords. Returns matched keyword or None."""
    text_lower = text.lower()
    for keyword in keywords:
        if keyword.lower() in text_lower:
            return keyword
    return None


def pre_filter_article(title: str, summary: str) -> FilterResult:
    """
    Pre-filter article based on keywords before sending to Gemini.
    Returns { "passed": bool, "reason": str or None }
    """
    text = f"{title} {summary}"

    # Check negative keywords
    for category, keywords in NEGATIVE_KEYWORDS.items():
        matched = check_keywords(text, keywords)
        if matched:
            return FilterResult(
                passed=False,
                reason=f"keyword_{category}:{matched}"
            )

    # Check trivial keywords
    for category, keywords in TRIVIAL_KEYWORDS.items():
        matched = check_keywords(text, keywords)
        if matched:
            return FilterResult(
                passed=False,
                reason=f"keyword_trivial:{matched}"
            )

    return FilterResult(passed=True, reason=None)
