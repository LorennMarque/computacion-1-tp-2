from flask import Flask, jsonify, render_template

from app.stats import load_current_stats, load_stats_history, redis_client

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
    return jsonify(
        {
            "datetime": stats["datetime"],
            "cpu_percent_total": cpu,
            "idle_percent": round(100 - cpu, 2),
            "cpu_percent_per_core": [float(p) for p in per_core],
        }
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
