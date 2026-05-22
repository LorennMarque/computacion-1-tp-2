import os
from datetime import datetime
import psutil

def get_stats():
    return {
        "datetime": datetime.now().isoformat(),
        "cpu_percent_total": psutil.cpu_percent(interval=0.5),
    }


for i in range(10):
    print(get_stats())