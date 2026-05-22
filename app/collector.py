from app.stats import get_stats, redis_client, save_stats


def run_collector():
    r = redis_client()
    while True:
        save_stats(r, get_stats())
