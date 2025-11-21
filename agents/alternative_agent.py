"""Alternative & Availability Agent

Suggests alternatives and checks availability using price tools.
"""
from typing import Dict, Any
from real_time_shopping_assistant.tools.price_tool import price_search_tool, check_stock_tool
from real_time_shopping_assistant.utils.langchain_compat import Tool


async def run_alternative_agent(product_id: str) -> Dict[str, Any]:
    listings = await price_search_tool._arun(product_id)
    # Suggest alternatives: pick second-cheapest or different seller
    sorted_l = sorted(listings, key=lambda x: x['price']) if listings else []
    alternative = sorted_l[1] if len(sorted_l) > 1 else (sorted_l[0] if sorted_l else None)
    stock_checks = []
    for l in (sorted_l[:3] if sorted_l else []):
        stock = await check_stock_tool._arun({"seller": l['seller'], "product_id": product_id})
        stock_checks.append(stock)

    availability_score = 0.0
    if stock_checks:
        scores = [1.0 if s['availability']=="in_stock" else 0.6 if s['availability']=="limited" else 0.0 for s in stock_checks]
        availability_score = round(sum(scores)/len(scores), 3)

    return {
        "alternative": alternative,
        "stock_checks": stock_checks,
        "availability_score": availability_score,
        "listings": listings,
    }


alternative_agent_tool = Tool.from_function(
    func=run_alternative_agent,
    name="alternative_agent",
    description="Suggests alternatives and checks stock/ETA.",
)
