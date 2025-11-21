"""Evaluator: synthetic simulation runner and report generator.

Generates synthetic events (many) and runs orchestrator offline, collecting metrics
and producing CSV + markdown summary report with simple charts.
"""
import asyncio
import csv
import os
import json
import random
from datetime import datetime, timezone
from typing import List
import matplotlib.pyplot as plt
from agents.loop_orchestrator import orchestrator
from infra.metrics import METRICS_FILE
from infra.logging_setup import logger


def generate_synthetic_events(n: int = 1000, out_path: str | None = None) -> List[dict]:
    events = []
    for i in range(n):
        user = f"user_{random.randint(1,200)}"
        price = round(random.uniform(5, 1200), 2)
        pid = f"prod_{random.randint(1000, 3000)}"
        ev = {
            "event_id": f"sim_{i}",
            "type": random.choice(["cart_add", "wishlist_add", "price_alert"]),
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "product_id": pid,
            "product_name": f"Product {pid}",
            "price": price,
            "user_id": user,
        }
        events.append(ev)
    if out_path:
        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(events, f, indent=2)
    return events


async def run_simulation(events: List[dict], batch: int = 100):
    # Run orchestrator on events in small batches to avoid memory pressure in demo
    results = []
    total = len(events)
    for i in range(0, total, batch):
        batch_events = events[i:i+batch]
        await orchestrator.run_loop(batch_events, stop_after=None)
    logger.info("Simulation complete")


def summarize_metrics(metrics_csv: str = METRICS_FILE, out_prefix: str = "eval_report"):
    # Read metrics CSV and produce summary
    if not os.path.exists(metrics_csv):
        logger.warning("No metrics file found: %s", metrics_csv)
        return
    df_rows = []
    with open(metrics_csv, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for r in reader:
            df_rows.append(r)
    # Basic metrics
    buys = sum(1 for r in df_rows if float(r.get("avg_buy_score",0))>=0.6)
    total = len(df_rows)
    buy_ratio = buys / total if total else 0
    # Save summary
    md = f"# Evaluation Summary\n\n- Total iterations: {total}\n- Buy ratio: {buy_ratio:.3f}\n"
    md_path = f"{out_prefix}.md"
    with open(md_path, "w", encoding="utf-8") as f:
        f.write(md)
    logger.info("Wrote evaluation summary to %s", md_path)


if __name__ == "__main__":
    events = generate_synthetic_events(200, out_path="synthetic_eval_events.json")
    asyncio.run(run_simulation(events, batch=50))
    summarize_metrics()
