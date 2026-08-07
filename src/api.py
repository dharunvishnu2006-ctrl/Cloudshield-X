import os
from flask import Flask, jsonify, request
from src.store import get_connection
from src.logging_setup import get_logger, setup_logging
from src.scanner_pipeline import build_scanner_pipeline
from src.reports import top_attackers, ip_profile, propagation_trace
from src.analytics_v2 import daily_trend_with_running_total
from src.attack_graph import load_graph_from_db
from src.schemas import ScanRequest, PlanRequest
from src.planner import prioritize
from src.lru_cache import LRUCache
from src.health import build_health_report
from flasgger import Swagger

profile_cache = LRUCache(capacity=100)


def get_cached_profile(ip: str) -> list:
    """Return an IP's profile, using the cache before hitting the database."""
    cached = profile_cache.get(ip)

    if cached is not None:
        return cached

    fresh = ip_profile(ip)
    profile_cache.put(ip, fresh)
    return fresh


setup_logging()
logger = get_logger("api")

app = Flask(__name__)
swagger = Swagger(app)


@app.route("/alerts", methods=["GET"])
def get_alerts():
    """Return alerts from v1.1's detection log.
    ---
    parameters:
      - name: severity
        in: query
        type: string
        required: false
      - name: since
        in: query
        type: string
        required: false
      - name: limit
        in: query
        type: integer
        required: false
        default: 100
    responses:
      200:
        description: A list of alerts
      400:
        description: limit out of range
    """
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
    """Run the F8 scanner pipeline on a log file inside data/.
    ---
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            log_path:
              type: string
              example: data/sample_server.log
            threshold:
              type: integer
              default: 3
    responses:
      200:
        description: Number of events inserted
      400:
        description: Invalid or unsafe log_path
    """
    try:
        payload = ScanRequest(**request.get_json())
    except Exception as e:
        return jsonify({"error": str(e)}), 400

    pipeline = build_scanner_pipeline()
    count = pipeline.run(payload.log_path)
    return jsonify({"events_inserted": count}), 200


@app.route("/threats", methods=["GET"])
def get_threats():
    """Return the top attacking IPs, ranked by hit count.
    ---
    parameters:
      - name: limit
        in: query
        type: integer
        required: false
        default: 10
    responses:
      200:
        description: A list of IPs with hits and average severity
    """
    limit = request.args.get("limit", 10, type=int)
    results = top_attackers(min_hits=0, limit=limit)
    return jsonify(results), 200


@app.route("/threats/<ip>", methods=["GET"])
def get_threat_profile(ip):
    """Return the full event history for one IP, using the LRU cache.
    ---
    parameters:
      - name: ip
        in: path
        type: string
        required: true
    responses:
      200:
        description: Event history for this IP
      404:
        description: No events found for this IP
    """
    results = get_cached_profile(ip)
    if not results:
        return jsonify({"error": "no events found for this ip"}), 404
    return jsonify(results), 200


@app.route("/trend", methods=["GET"])
def get_trend():
    """Return daily event counts with a running total and 7-day average.
    ---
    responses:
      200:
        description: Daily trend data
    """
    results = daily_trend_with_running_total()
    return jsonify(results), 200


@app.route("/propagation", methods=["GET"])
def get_propagation():
    """Trace every host reachable from a starting host, via a recursive CTE.
    ---
    parameters:
      - name: host
        in: query
        type: string
        required: true
    responses:
      200:
        description: Reachable hosts with hop counts
      400:
        description: Missing host parameter
    """
    host = request.args.get("host")

    if not host:
        return jsonify({"error": "host query parameter is required"}), 400

    results = propagation_trace(host)
    return jsonify(results), 200


@app.route("/graph/paths", methods=["GET"])
def get_graph_paths():
    """Find a valid path between two hosts using DFS.
    ---
    parameters:
      - name: source
        in: query
        type: string
        required: true
      - name: target
        in: query
        type: string
        required: true
    responses:
      200:
        description: A valid path from source to target
      400:
        description: Missing source or target
      404:
        description: No path found
    """
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
    """Find the cheapest path between two hosts using Dijkstra.
    ---
    parameters:
      - name: source
        in: query
        type: string
        required: true
      - name: target
        in: query
        type: string
        required: true
    responses:
      200:
        description: The cheapest path and its total cost
      400:
        description: Missing source or target
      404:
        description: No path found
    """
    source = request.args.get("source")
    target = request.args.get("target")

    if not source or not target:
        return jsonify({"error": "source and target are required"}), 400

    graph = load_graph_from_db()
    path, cost = graph.dijkstra(source, target)

    if not path:
        return jsonify({"error": "no path found"}), 404
    return jsonify({"path": path, "cost": cost}), 200


@app.route("/plan", methods=["POST"])
def get_plan():
    """Choose which threats to mitigate inside a budget, using 0/1 knapsack.
    ---
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            threats:
              type: array
              example: [["sql_injection", 9, 3], ["port_scan", 4, 1]]
            budget:
              type: integer
              example: 5
    responses:
      200:
        description: Total risk reduced and the chosen threats
      400:
        description: Invalid request body
    """
    try:
        payload = PlanRequest(**request.get_json())
    except Exception as e:
        return jsonify({"error": str(e)}), 400

    try:
        threats = [tuple(t) for t in payload.threats]
        total, chosen = prioritize(threats, payload.budget)
    except Exception as e:
        return jsonify({"error": f"invalid threats format: {e}"}), 400

    return jsonify({"total_risk_reduced": total, "chosen": chosen}), 200


@app.route("/health", methods=["GET"])
def health_check():
    """Return a genuine health report - database, tables, index, cache, uptime.
    ---
    responses:
      200:
        description: Everything is healthy
      503:
        description: Database is down
    """
    report = build_health_report()
    status_code = 503 if report["database"] == "down" else 200
    return jsonify(report), status_code


if __name__ == "__main__":
    debug_mode = os.environ.get("FLASK_DEBUG", "False") == "True"
    app.run(debug=debug_mode, port=5000)
