import os
from datetime import datetime
import psutil
import redis
import json

r = redis.Redis(host='localhost', port=6379, db=0)

def get_stats():
    return {
        "datetime": datetime.now().isoformat(),
        "cpu_percent_total": psutil.cpu_percent(interval=0.1),
    }


def save_stats(stats):
    r.set(f"stats:{stats['datetime']}", json.dumps(stats), ex=60)


# Listar todas las claves y valores
def show_all_keys_and_values():
    keys = r.keys('*')
    for key in keys:
        print(key, r.get(key))


for i in range(10):
    save_stats(get_stats())

print("===========================================")
show_all_keys_and_values()