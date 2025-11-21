"""Demo script: runs the orchestrator on synthetic events.

This script demonstrates the loop for synthetic events. If a `synthetic_transactions.json`
file is not present, it will auto-generate a small batch of events for the demo.
"""
import asyncio
import json
import os
import random
import sys
from pathlib import Path

# Ensure package can be imported when running demo.py directly
repo_root = Path(__file__).resolve().parent.parent
if str(repo_root) not in sys.path:
    sys.path.insert(0, str(repo_root))

from real_time_shopping_assistant.agents.loop_orchestrator import orchestrator
from real_time_shopping_assistant.infra.logging_setup import logger


def load_synthetic_events(path="synthetic_transactions.json"):
    # Prefer package-local file
    candidate = path
    if not os.path.isabs(candidate):
        candidate = os.path.join(os.path.dirname(__file__), path)
        if not os.path.exists(candidate):
            candidate = path
    if os.path.exists(candidate):
        with open(candidate, "r", encoding="utf-8") as f:
            return json.load(f)
    return []


def generate_synthetic_events(n=10):
    events = []
    for i in range(n):
        user = f"user_{random.randint(1,50)}"
        price = round(random.uniform(5, 500), 2)
        pid = f"prod_{random.randint(1000, 2000)}"
        ev = {
            "event_id": f"demo_{i}",
            "type": random.choice(["cart_add", "wishlist_add", "price_alert"]),
            "timestamp": None,
            "product_id": pid,
            "product_name": f"Product {pid}",
            "price": price,
            "user_id": user,
        }
        events.append(ev)
    return events


async def run_demo():
    events = load_synthetic_events()
    if not events:
        logger.info("No synthetic events file found — generating demo events.")
        events = generate_synthetic_events(10)
    await orchestrator.run_loop(events, stop_after=len(events))


if __name__ == "__main__":
    asyncio.run(run_demo())
