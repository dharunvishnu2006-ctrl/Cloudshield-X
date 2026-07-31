from flask import Flask, jsonify, request
from src.store import get_connection
from src.logging_setup import get_logger, setup_logging

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
    app.run(debug=True, port=5000)
