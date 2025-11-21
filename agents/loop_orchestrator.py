"""Loop Orchestrator

Orchestrates ingestion of events, calls agents (possibly in parallel), records memory and logs.
Uses async execution and demonstrates LangChain AgentExecutor patterns in concept.
"""
import asyncio
from typing import Dict, Any
import time
import json
from real_time_shopping_assistant.infra.logging_setup import logger
from real_time_shopping_assistant.infra.metrics import record_metrics
from real_time_shopping_assistant.memory.short_term_memory import create_short_term_memory
from real_time_shopping_assistant.memory.long_term_memory import long_term_memory

from real_time_shopping_assistant.tools.cart_tool import tool as cart_tool
from real_time_shopping_assistant.tools.profile_tool import tool as profile_tool
from real_time_shopping_assistant.agents.price_agent import price_agent_tool
from real_time_shopping_assistant.agents.review_agent import review_agent_tool
from real_time_shopping_assistant.agents.user_finance_agent import user_finance_tool
from real_time_shopping_assistant.agents.alternative_agent import alternative_agent_tool
from real_time_shopping_assistant.agents.fusion_agent import fusion_agent_tool


class LoopOrchestrator:
    def __init__(self):
        self.short_memory = create_short_term_memory()
        self.long_memory = long_term_memory
        self.iteration = 0
        self._running = False

    async def ingest_event(self, event: Dict[str, Any]) -> Dict[str, Any]:
        # Basic ingestion: orchestrate multiple agent calls and fuse
        t0 = time.time()
        user_id = event.get("user_id")
        product_id = event.get("product_id")
        price = event.get("price")

        # Fetch profile and cart concurrently
        profile_task = asyncio.create_task(profile_tool._arun(user_id))
        cart_task = asyncio.create_task(cart_tool._arun(user_id))
        price_task = asyncio.create_task(price_agent_tool.run(product_id)) if hasattr(price_agent_tool, 'run') else asyncio.create_task(price_agent_tool.func(product_id))

        # For tools created via Tool.from_function, call .func (async function)
        profile_json = await profile_task
        cart_json = await cart_task
        price_out = await price_task

        # Call other agents
        review_task = asyncio.create_task(review_agent_tool.func(product_id))
        finance_task = asyncio.create_task(user_finance_tool.func(profile_json, price))
        alternative_task = asyncio.create_task(alternative_agent_tool.func(product_id))

        review_out = await review_task
        finance_out = await finance_task
        alt_out = await alternative_task

        # Build components and evidence
        components = {
            "affordability_score": finance_out.get("affordability_score"),
            "price_attractiveness": price_out.get("price_attractiveness"),
            "sentiment_score": review_out.get("sentiment_score"),
            "availability_score": alt_out.get("availability_score"),
            "preference_score": 0.5,  # placeholder: could use profile preferences
            "evidence": {
                "price": price_out,
                "reviews": review_out.get("reviews"),
                "alt": alt_out,
                "finance_reasoning": finance_out.get("reasoning"),
            },
        }

        decision = fusion_agent_tool.func(components)

        # Update memories
        self.short_memory.save_context({"input": event}, {"output": decision})
        # long-term memory: store the event and decision as a document
        # vectorstore insertion simplified: use memory.retriever.store? for demo we skip

        loop_time = round(time.time() - t0, 3)
        # metrics
        record_metrics(loop_time, 1, 1.0 if decision.get('decision')=='BUY' else 0.0, decision.get('buy_score'))

        self.iteration += 1
        logger.info(json.dumps({"event_id": event.get("event_id"), "decision": decision}))
        return decision

    async def run_loop(self, event_stream, stop_after: int | None = None):
        self._running = True
        processed = 0
        for event in event_stream:
            if not self._running:
                break
            await self.ingest_event(event)
            processed += 1
            if stop_after and processed >= stop_after:
                break
            await asyncio.sleep(0.2)  # poll pause
        self._running = False

    def stop(self):
        self._running = False


# Factory
orchestrator = LoopOrchestrator()
