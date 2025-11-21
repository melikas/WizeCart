"""Review & Sentiment Agent

This agent fetches reviews and computes a sentiment_score using a simple
lexicon-based fallback, with optional LLM-based analysis placeholder.
"""
from typing import Dict, Any, List
from real_time_shopping_assistant.tools.reviews_tool import get_reviews_tool
from real_time_shopping_assistant.utils.langchain_compat import Tool

POSITIVE_WORDS = {"excellent","great","recommend","comfortable","good","love"}
NEGATIVE_WORDS = {"disappointed","poor","stopped","bad","terrible","problem"}


def lexicon_sentiment_score(reviews: List[Dict[str, Any]]) -> float:
    if not reviews:
        return 0.5
    score_sum = 0.0
    for r in reviews:
        text = r.get("text", "").lower()
        s = 0.5
        for w in POSITIVE_WORDS:
            if w in text:
                s += 0.1
        for w in NEGATIVE_WORDS:
            if w in text:
                s -= 0.15
        score_sum += max(0.0, min(1.0, s))
    return round(score_sum / len(reviews), 3)


async def run_review_agent(product_id: str) -> Dict[str, Any]:
    reviews = await get_reviews_tool._arun(product_id)
    sentiment = lexicon_sentiment_score(reviews)
    return {"reviews": reviews, "sentiment_score": sentiment}


review_agent_tool = Tool.from_function(
    func=run_review_agent,
    name="review_agent",
    description="Analyzes reviews and returns a sentiment score and reviews.",
)
