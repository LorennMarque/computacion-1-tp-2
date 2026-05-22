import json
from datetime import datetime

import psutil
import redis

REDIS_HOST = "localhost"
REDIS_PORT = 6379
REDIS_DB = 0
CURRENT_KEY = "stats:current"
REFRESH_INTERVAL_SEC = 0.05
COLLECT_INTERVAL_SEC = REFRESH_INTERVAL_SEC


def redis_client():
    return redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB)


def get_stats():
    per_core = psutil.cpu_percent(percpu=True, interval=REFRESH_INTERVAL_SEC)
    total = round(sum(per_core) / len(per_core), 2) if per_core else 0.0
    return {
        "datetime": datetime.now().isoformat(),
        "cpu_percent_total": total,
        "cpu_percent_per_core": [round(p, 2) for p in per_core],
    }


def save_stats(r, stats):
    payload = json.dumps(stats)
    r.set(f"stats:{stats['datetime']}", payload, ex=60)
    r.set(CURRENT_KEY, payload)


def load_current_stats(r):
    raw = r.get(CURRENT_KEY)
    if raw is None:
        return None
    return json.loads(raw)


def _redis_key(key):
    return key.decode() if isinstance(key, bytes) else key


def load_stats_history(r):
    keys = r.keys("stats:*")
    points = []
    for key in keys:
        if _redis_key(key) == CURRENT_KEY:
            continue
        raw = r.get(key)
        if raw is None:
            continue
        stats = json.loads(raw)
        points.append(
            {
                "datetime": stats["datetime"],
                "cpu_percent_total": float(stats["cpu_percent_total"]),
            }
        )
    points.sort(key=lambda p: p["datetime"])
    return points
