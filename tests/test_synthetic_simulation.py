"""Unit tests for the synthetic simulation and scoring functions."""
import asyncio
from real_time_shopping_assistant.agents.fusion_agent import fusion_decision
from real_time_shopping_assistant.agents.user_finance_agent import affordability_score


def test_affordability_easy():
    profile = {"current_balance": 1000.0, "monthly_budget": 800.0}
    score = affordability_score(profile, 100.0)
    assert score > 0.7


def test_fusion_high_buy():
    components = {"affordability_score": 0.9, "price_attractiveness": 0.9, "sentiment_score": 0.9, "availability_score": 1.0, "preference_score":0.8}
    out = fusion_decision(components)
    assert out["decision"] == "BUY"


if __name__ == "__main__":
    test_affordability_easy()
    test_fusion_high_buy()
    print("Tests passed")
