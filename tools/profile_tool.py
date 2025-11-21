"""Tool: get_user_profile

Returns user financial profile, preferences, budget constraints.
"""
from typing import Dict, Any
from pydantic import BaseModel
import asyncio
from langchain.tools import BaseTool
from tenacity import retry, stop_after_attempt, wait_exponential


class ProfileSchema(BaseModel):
    user_id: str
    monthly_budget: float
    current_balance: float
    loyalty_tier: str
    preferences: Dict[str, Any]


class GetUserProfileTool(BaseTool):
    name: str = "get_user_profile"
    description: str = "Returns user profile with budget and preferences."

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=0.2, max=2))
    async def _arun(self, user_id: str) -> str:
        await asyncio.sleep(0.02)
        sample = {
            "user_id": user_id,
            "monthly_budget": 800.0,
            "current_balance": 250.0,
            "loyalty_tier": "gold",
            "preferences": {"brands": ["BrandA"], "avoid_categories": ["expensive_gadgets"]},
        }
        return ProfileSchema(**sample).json()

    def _run(self, user_id: str) -> str:
        return asyncio.get_event_loop().run_until_complete(self._arun(user_id))


tool = GetUserProfileTool()
