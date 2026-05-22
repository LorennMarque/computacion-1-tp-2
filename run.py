import multiprocessing

from app.collector import run_collector
from app.web import app


def run_web():
    app.run(host="0.0.0.0", port=5003, debug=False, use_reloader=False)


if __name__ == "__main__":
    multiprocessing.set_start_method("spawn", force=True)
    collector = multiprocessing.Process(target=run_collector, name="collector")
    web = multiprocessing.Process(target=run_web, name="web")

    collector.start()
    web.start()

    try:
        collector.join()
        web.join()
    except KeyboardInterrupt:
        collector.terminate()
        web.terminate()
        collector.join()
        web.join()
