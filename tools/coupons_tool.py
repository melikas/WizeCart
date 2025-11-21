"""Tool: get_coupons

Returns applicable coupons and estimated savings.
"""
from typing import List, Dict, Any
import asyncio
from pydantic import BaseModel
from tenacity import retry, stop_after_attempt, wait_exponential
from langchain.tools import BaseTool
import random


class Coupon(BaseModel):
    code: str
    discount_pct: float
    expires_in_days: int


class CouponsTool(BaseTool):
    name: str = "get_coupons"
    description: str = "Return coupons applicable to a product."

    @retry(stop=stop_after_attempt(2), wait=wait_exponential(multiplier=0.2, max=1))
    async def _arun(self, product_id: str) -> List[Dict[str, Any]]:
        await asyncio.sleep(0.02)
        coupons = []
        if random.random() > 0.6:
            coupons.append(Coupon(code="SAVE10", discount_pct=10.0, expires_in_days=7).dict())
        if random.random() > 0.85:
            coupons.append(Coupon(code="FREESHIP", discount_pct=0.0, expires_in_days=2).dict())
        return coupons

    def _run(self, product_id: str):
        return asyncio.get_event_loop().run_until_complete(self._arun(product_id))


coupons_tool = CouponsTool()
