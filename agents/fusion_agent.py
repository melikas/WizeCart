"""Decision Fusion Agent

Consumes structured outputs from other agents and computes BUY_SCORE and final decision.
This is implemented as a deterministic function and is exposed as a LangChain tool.
"""
from typing import Dict, Any
from real_time_shopping_assistant.utils.langchain_compat import Tool
from real_time_shopping_assistant.config.settings import settings
from datetime import datetime, timezone


def compute_buy_score(component_scores: Dict[str, float]) -> float:
    # Apply weights from settings
    w_aff = settings.WEIGHT_AFFORDABILITY
    w_price = settings.WEIGHT_PRICE
    w_sent = settings.WEIGHT_SENTIMENT
    w_avail = settings.WEIGHT_AVAILABILITY
    w_pref = settings.WEIGHT_PREFERENCE

    score = (
        component_scores.get("affordability_score", 0) * w_aff +
        component_scores.get("price_attractiveness", 0) * w_price +
        component_scores.get("sentiment_score", 0) * w_sent +
        component_scores.get("availability_score", 0) * w_avail +
        component_scores.get("preference_score", 0) * w_pref
    )
    return round(score, 4)


def fusion_decision(components: Dict[str, Any]) -> Dict[str, Any]:
    # components expected to include numeric component scores
    comp_scores = {
        "affordability_score": components.get("affordability_score", 0.0),
        "price_attractiveness": components.get("price_attractiveness", 0.0),
        "sentiment_score": components.get("sentiment_score", 0.5),
        "availability_score": components.get("availability_score", 0.0),
        "preference_score": components.get("preference_score", 0.5),
    }
    buy_score = compute_buy_score(comp_scores)
    if buy_score >= settings.BUY_THRESHOLD:
        decision = "BUY"
        action = "add_to_cart"
    elif buy_score >= 0.4:
        decision = "DEFER"
        action = "wait_for_deal"
    else:
        decision = "NOT_BUY"
        action = "choose_alternative"

    out = {
        "decision": decision,
        "buy_score": buy_score,
        "component_scores": comp_scores,
        "reasoning": f"Weighted fusion on components -> buy_score={buy_score}",
        "recommended_action": action,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }
    # include evidence if present
    if "evidence" in components:
        out["evidence"] = components["evidence"]
    return out


fusion_agent_tool = Tool.from_function(
    func=fusion_decision,
    name="fusion_agent",
    description="Fuse agent outputs into a final BUY/NOT_BUY/DEFER decision.",
)
