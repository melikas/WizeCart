"""Tool: price_search, get_price_history, check_stock

These tools return synthetic price listings, history, and stock checks. They are async
and include retry/backoff logic for robustness.
"""
from typing import Any, Dict, List
import asyncio
from pydantic import BaseModel
from tenacity import retry, stop_after_attempt, wait_exponential
from langchain.tools import BaseTool
import random
import time


class PriceListing(BaseModel):
    seller: str
    price: float
    currency: str
    shipping: float
    timestamp: float


class PriceSearchTool(BaseTool):
    name: str = "price_search"
    description: str = "Search prices for a product across retailers. Returns JSON list of listings."

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=0.2, max=1))
    async def _arun(self, product_id_or_query: str) -> str:
        await asyncio.sleep(0.05)
        base = 100.0 + random.uniform(-30, 80)
        listings = []
        for seller in ["RetailerA", "RetailerB", "RetailerC"]:
            listings.append(PriceListing(
                seller=seller,
                price=round(base * random.uniform(0.9, 1.2), 2),
                currency="USD",
                shipping=round(random.uniform(0, 10), 2),
                timestamp=time.time(),
            ).dict())
        return listings

    def _run(self, product_id_or_query: str) -> List[Dict[str, Any]]:
        return asyncio.get_event_loop().run_until_complete(self._arun(product_id_or_query))


class PriceHistoryTool(BaseTool):
    name: str = "get_price_history"
    description: str = "Return a simple price time series for the product."

    @retry(stop=stop_after_attempt(2), wait=wait_exponential(multiplier=0.2, max=1))
    async def _arun(self, product_id: str) -> str:
        await asyncio.sleep(0.02)
        # Simple synthetic history
        now = int(time.time())
        history = [{"ts": now - i * 86400, "price": round(100 + (i % 10) * 2 + random.uniform(-5, 5), 2)} for i in range(30)]
        return history

    def _run(self, product_id: str):
        return asyncio.get_event_loop().run_until_complete(self._arun(product_id))


class CheckStockTool(BaseTool):
    name: str = "check_stock"
    description: str = "Check stock for a product at a seller. Returns availability and ETA."

    @retry(stop=stop_after_attempt(2), wait=wait_exponential(multiplier=0.1, max=1))
    async def _arun(self, payload: dict) -> dict:
        # payload: {"seller":..., "product_id":...}
        await asyncio.sleep(0.01)
        availability = random.choice(["in_stock", "limited", "out_of_stock"])
        eta_days = 0 if availability == "in_stock" else random.choice([2,5,10])
        return {"seller": payload.get("seller"), "product_id": payload.get("product_id"), "availability": availability, "eta_days": eta_days}

    def _run(self, payload: dict) -> dict:
        return asyncio.get_event_loop().run_until_complete(self._arun(payload))

# Export tool instances for LangChain usage
price_search_tool = PriceSearchTool()
price_history_tool = PriceHistoryTool()
check_stock_tool = CheckStockTool()
