"""User Finance & Preference Agent

Implements a LangChain Chain that evaluates affordability, budget constraints, and loyalty.
"""
from real_time_shopping_assistant.utils.langchain_compat import Tool
from typing import Dict, Any
import json

# This agent can use an LLMChain to generate human-readable reasoning,
# but uses deterministic scoring for affordability.


def affordability_score(user_profile: Dict[str, Any], price: float) -> float:
    # Simple rule-based affordability scoring
    balance = user_profile.get("current_balance", 0.0)
    monthly = user_profile.get("monthly_budget", 0.0)
    # Score 0-1: prefers purchases well within balance and budget
    if price <= balance * 0.5 and price <= monthly * 0.3:
        return 0.95
    if price <= balance and price <= monthly * 0.6:
        return 0.7
    if price <= balance * 1.2:
        return 0.4
    return 0.05


async def run_user_finance_agent(profile_json: str, price: float) -> Dict[str, Any]:
    profile = json.loads(profile_json)
    score = affordability_score(profile, price)
    reasoning = f"Affordability evaluated: balance={profile.get('current_balance')} monthly_budget={profile.get('monthly_budget')} price={price} -> score={score}"
    return {"affordability_score": score, "reasoning": reasoning, "profile": profile}

# Expose as tool-compatible callable
user_finance_tool = Tool.from_function(
    func=run_user_finance_agent,
    name="user_finance_agent",
    description="Evaluates user affordability and preferences.",
)
