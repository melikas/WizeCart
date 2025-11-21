"""Tool: get_user_cart

Async LangChain-style Tool that returns synthetic cart JSON or loads from a data source.
"""
from typing import Dict, Any
from pydantic import BaseModel
import asyncio
import json
import os

from langchain.tools import BaseTool
from tenacity import retry, stop_after_attempt, wait_exponential


class CartSchema(BaseModel):
    user_id: str
    items: list[Dict[str, Any]]


class GetUserCartTool(BaseTool):
    name: str = "get_user_cart"
    description: str = "Returns the current user's cart as structured JSON."

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=0.5, max=4))
    async def _arun(self, query: str | None = None) -> str:
        # Simulate async fetch; in production, call DB or API
        await asyncio.sleep(0.05)
        sample = {
            "user_id": "user_001",
            "items": [
                {"product_id": "prod_1001", "name": "Wireless Headphones Model X", "price": 129.99, "qty": 1}
            ],
        }
        return CartSchema(**sample).json()

    def _run(self, query: str | None = None) -> str:
        return asyncio.get_event_loop().run_until_complete(self._arun(query))


tool = GetUserCartTool()
