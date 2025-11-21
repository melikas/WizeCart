"""Simple metrics exporter (CSV fallback) and counters.

This file provides a minimal Prometheus-like metric recorder that writes
periodically to CSV for easy inspection in the demo environment.
"""
import csv
import os
from datetime import datetime
from threading import Lock

METRICS_FILE = os.path.join(os.getcwd(), "metrics.csv")
_lock = Lock()

metrics_schema = [
    "timestamp",
    "loop_iteration_time",
    "events_processed",
    "buy_ratio",
    "avg_buy_score",
]


def init_metrics():
    if not os.path.exists(METRICS_FILE):
        with open(METRICS_FILE, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(metrics_schema)


def record_metrics(loop_iteration_time, events_processed, buy_ratio, avg_buy_score):
    row = [
        datetime.utcnow().isoformat() + "Z",
        loop_iteration_time,
        events_processed,
        buy_ratio,
        avg_buy_score,
    ]
    with _lock:
        with open(METRICS_FILE, "a", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(row)


init_metrics()
