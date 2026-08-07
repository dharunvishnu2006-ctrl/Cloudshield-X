import os
from flask import Flask, jsonify, request
from src.store import get_connection
from src.logging_setup import get_logger, setup_logging
from src.schemas import ScanRequest
from src.scanner_pipeline import build_scanner_pipeline
from src.reports import top_attackers, ip_profile, propagation_trace
from src.analytics_v2 import daily_trend_with_running_total
from src.attack_graph import load_graph_from_db

setup_logging()
logger = get_logger("api")

app = Flask(__name__)


@app.route("/alerts", methods=["GET"])
def get_alerts():
    severity = request.args.get("severity")
    since = request.args.get("since")
    limit = request.args.get("limit", 100, type=int)

    if limit < 1 or limit > 1000:
        return jsonify({"error": "limit must be between 1 and 1000"}), 400

    try:
        with get_connection() as conn:
            query = "SELECT * FROM alerts WHERE 1=1"
            params = []

            if severity:
                query += " AND severity = ?"
                params.append(severity)

            if since:
                query += " AND at >= ?"
                params.append(since)

            query += " ORDER BY at DESC LIMIT ?"
            params.append(limit)

            cursor = conn.execute(query, params)
            alerts = [dict(row) for row in cursor.fetchall()]

        logger.info(f"GET /alerts → {len(alerts)} results")
        return jsonify(alerts), 200

    except Exception as e:
        logger.error(f"GET /alerts failed: {e}")
        return jsonify({"error": "internal error"}), 500


@app.route("/scan", methods=["POST"])
def scan_log():
    try:
        payload = ScanRequest(**request.get_json())
    except Exception as e:
        return jsonify({"error": str(e)}), 400

    pipeline = build_scanner_pipeline()
    count = pipeline.run(payload.log_path)
    return jsonify({"events_inserted": count}), 200


@app.route("/threats", methods=["GET"])
def get_threats():
    limit = request.args.get("limit", 10, type=int)
    results = top_attackers(min_hits=0, limit=limit)
    return jsonify(results), 200


@app.route("/threats/<ip>", methods=["GET"])
def get_threat_profile(ip):
    results = ip_profile(ip)
    if not results:
        return jsonify({"error": "no events found for this ip"}), 404
    return jsonify(results), 200


@app.route("/trend", methods=["GET"])
def get_trend():
    results = daily_trend_with_running_total()
    return jsonify(results), 200


@app.route("/propagation", methods=["GET"])
def get_propagation():
    host = request.args.get("host")

    if not host:
        return jsonify({"error": "host query parameter is required"}), 400

    results = propagation_trace(host)
    return jsonify(results), 200


@app.route("/graph/paths", methods=["GET"])
def get_graph_paths():
    source = request.args.get("source")
    target = request.args.get("target")

    if not source or not target:
        return jsonify({"error": "source and target are required"}), 400

    graph = load_graph_from_db()
    path = graph.dfs(source, target)

    if not path:
        return jsonify({"error": "no path found"}), 404
    return jsonify({"path": path}), 200


@app.route("/graph/cheapest", methods=["GET"])
def get_graph_cheapest():
    source = request.args.get("source")
    target = request.args.get("target")

    if not source or not target:
        return jsonify({"error": "source and target are required"}), 400

    graph = load_graph_from_db()
    path, cost = graph.dijkstra(source, target)

    if not path:
        return jsonify({"error": "no path found"}), 404
    return jsonify({"path": path, "cost": cost}), 200


@app.route("/health", methods=["GET"])
def health_check():
    try:
        with get_connection() as conn:
            cursor = conn.execute("SELECT COUNT(*) as count FROM alerts")
            alert_count = cursor.fetchone()["count"]

            cursor = conn.execute("SELECT MAX(at) as last_scan FROM alerts")
            last_scan = cursor.fetchone()["last_scan"]

        return (
            jsonify(
                {
                    "status": "ok",
                    "alert_count": alert_count,
                    "last_scan": last_scan,
                    "db": "connected",
                }
            ),
            200,
        )

    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return jsonify({"status": "error", "db": "disconnected", "error": str(e)}), 500


if __name__ == "__main__":
    debug_mode = os.environ.get("FLASK_DEBUG", "False") == "True"
    app.run(debug=debug_mode, port=5000)
