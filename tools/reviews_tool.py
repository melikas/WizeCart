"""Tool: get_reviews

Returns synthetic reviews and demonstrates a deterministic sentiment fallback.
"""
from typing import List, Dict, Any
import asyncio
from pydantic import BaseModel
from tenacity import retry, stop_after_attempt, wait_exponential
from langchain.tools import BaseTool
import random


class Review(BaseModel):
    review_id: str
    rating: int
    text: str
    timestamp: float


class GetReviewsTool(BaseTool):
    name: str = "get_reviews"
    description: str = "Return raw reviews and metadata for a product."

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=0.2, max=1))
    async def _arun(self, product_id: str) -> List[Dict[str, Any]]:
        await asyncio.sleep(0.03)
        # generate synthetic reviews
        sample_texts = [
            "Excellent sound quality and battery life.",
            "Stopped working after a week, disappointed.",
            "Great value for price. Highly recommend.",
            "Mediocre build and poor customer support.",
            "Comfortable to wear, noise cancellation decent.",
        ]
        reviews = []
        for i in range(20):
            text = random.choice(sample_texts)
            reviews.append(Review(review_id=f"r_{i}", rating=random.randint(1,5), text=text, timestamp=0).dict())
        return reviews

    def _run(self, product_id: str):
        return asyncio.get_event_loop().run_until_complete(self._arun(product_id))


get_reviews_tool = GetReviewsTool()
