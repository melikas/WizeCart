"""main.py - production entrypoint

Provides CLI to run in 'loop' mode or quick demo. Supports safe shutdown.
"""
import argparse
import asyncio
import signal
import json
import os
from infra.logging_setup import logger
from agents.loop_orchestrator import orchestrator


def load_events(path: str):
    # Resolve relative path against the package if needed
    candidate = path
    if not os.path.isabs(candidate):
        candidate = os.path.join(os.path.dirname(__file__), path)
        if not os.path.exists(candidate):
            candidate = path  # fallback to literal
    try:
        with open(candidate, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        logger.exception("Failed loading events: %s", candidate)
        return []


async def main_loop(events_path: str, stop_after: int | None = None):
    events = load_events(events_path)
    await orchestrator.run_loop(events, stop_after=stop_after)


def run():
    parser = argparse.ArgumentParser()
    default_events = os.path.join(os.path.dirname(__file__), "synthetic_transactions.json")
    parser.add_argument("--events", default=default_events)
    parser.add_argument("--stop-after", type=int, default=None)
    args = parser.parse_args()

    loop = asyncio.get_event_loop()

    def _signal_handler(sig, frame):
        logger.info("Signal received, stopping orchestrator")
        orchestrator.stop()

    signal.signal(signal.SIGINT, _signal_handler)
    signal.signal(signal.SIGTERM, _signal_handler)

    loop.run_until_complete(main_loop(args.events, args.stop_after))


if __name__ == "__main__":
    run()
