import json

from flask import Flask, Response, jsonify, render_template

from app.stats import (
    ALERT_CHANNEL,
    alert_payload,
    load_current_stats,
    load_stats_history,
    redis_client,
)

app = Flask(__name__, template_folder="../templates")


@app.route("/")
def dashboard():
    return render_template("dashboard.html")


@app.route("/api/cpu")
def api_cpu():
    stats = load_current_stats(redis_client())
    if stats is None:
        return jsonify({"error": "no data yet"}), 503
    cpu = float(stats["cpu_percent_total"])
    per_core = stats.get("cpu_percent_per_core", [])
    alert = alert_payload(stats)
    return jsonify(
        {
            "datetime": stats["datetime"],
            "cpu_percent_total": cpu,
            "idle_percent": round(100 - cpu, 2),
            "cpu_percent_per_core": [float(p) for p in per_core],
            "alert": alert["alert"],
            "per_core_high": alert["per_core_high"],
        }
    )


@app.route("/api/alert/subscribe")
def api_alert_subscribe():
    def generate():
        r = redis_client()
        stats = load_current_stats(r)
        if stats is not None:
            yield f"data: {json.dumps(alert_payload(stats))}\n\n"
        pubsub = r.pubsub()
        pubsub.subscribe(ALERT_CHANNEL)
        for message in pubsub.listen():
            if message["type"] != "message":
                continue
            data = message["data"]
            if isinstance(data, bytes):
                data = data.decode()
            yield f"data: {data}\n\n"

    return Response(
        generate(),
        mimetype="text/event-stream",
        headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"},
    )


@app.route("/api/cpu/history")
def api_cpu_history():
    points = load_stats_history(redis_client())
    if not points:
        return jsonify({"error": "no data yet"}), 503
    return jsonify(
        {
            "timestamps": [p["datetime"] for p in points],
            "cpu_percent_total": [p["cpu_percent_total"] for p in points],
        }
    )
