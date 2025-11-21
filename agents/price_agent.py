"""Price & Deal Agent

Uses price tools and simulation to estimate price attractiveness.
"""
from real_time_shopping_assistant.utils.langchain_compat import Tool
import json
from typing import Any, Dict

from real_time_shopping_assistant.tools.price_tool import price_search_tool, price_history_tool
from real_time_shopping_assistant.tools.coupons_tool import coupons_tool
from real_time_shopping_assistant.tools.code_exec_tool import code_exec_tool


async def run_price_agent(product_id: str) -> Dict[str, Any]:
    # Call price_search, get price_history, coupons, and run simulation
    listings = await price_search_tool._arun(product_id)
    history = await price_history_tool._arun(product_id)
    coupons = await coupons_tool._arun(product_id)
    current_price = min([l['price'] for l in listings]) if listings else 0.0
    sim = await code_exec_tool._arun({"current_price": current_price, "history": history})

    # compute price attractiveness: lower price + coupons + high prob_drop -> higher score
    coupon_savings = max([c['discount_pct'] for c in coupons], default=0.0)
    attractiveness = min(1.0, (1.0 - (current_price / (current_price + 100))) + coupon_savings / 100 + sim.get('probability_drop', 0))

    return {
        "price_listings": listings,
        "price_history": history,
        "coupons": coupons,
        "current_price": current_price,
        "simulation": sim,
        "price_attractiveness": round(attractiveness, 3),
    }


price_agent_tool = Tool.from_function(
    func=run_price_agent,
    name="price_agent",
    description="Analyzes prices, history, coupons, and simulates near-term drops.",
)
