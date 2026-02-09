"""
Flask application – Algorithm Analyzer
=======================================
Endpoints
---------
GET  /analyze           – run an algo analysis, return JSON + base-64 graph
POST /save_analysis     – persist an analysis result to MySQL, return its ID
GET  /retrieve_analysis – fetch a saved analysis by ID
"""
from flask import Flask, request, jsonify
from analyzer import run_analysis
from models import init_db, Session, AlgoAnalysis

app = Flask(__name__)

# Create the DB table on startup
init_db()


# ── 1. /analyze ──────────────────────────────────────────────────────
@app.route("/analyze")
def analyze():
    """
    GET /analyze?algo=bubble_sort&n=1000&steps=10

    Runs the requested algorithm for increasing values of n,
    measures execution time, and returns a JSON response that
    includes a base-64 encoded performance graph.
    """
    algo  = request.args.get("algo", "").strip().strip('"').strip("'")
    n     = request.args.get("n", type=int)
    steps = request.args.get("steps", type=int)

    if not algo or n is None or steps is None:
        return jsonify({"error": "Missing required query params: algo, n, steps"}), 400

    try:
        result = run_analysis(algo, n, steps)
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

    return jsonify(result), 200


# ── 2. /save_analysis (POST) ─────────────────────────────────────────
@app.route("/save_analysis", methods=["POST"])
def save_analysis():
    """
    POST /save_analysis
    Body (JSON):
    {
        "algo": "bubble_sort",
        "items": 1000,
        "steps": 10,
        "start_time": 1700000000.123,
        "end_time":   1700000003.456,
        "total_time_ms": 3333.0,
        "time_complexity": "O(n^2)",
        "graph_base64": "<base64 string>"
    }

    Saves the payload to the `algo_analysis` table and returns the new row ID.
    """
    data = request.get_json(silent=True)
    if not data:
        return jsonify({"error": "Request body must be valid JSON"}), 400

    required = ["algo", "items", "steps", "start_time",
                "end_time", "total_time_ms", "time_complexity", "graph_base64"]
    missing = [f for f in required if f not in data]
    if missing:
        return jsonify({"error": f"Missing fields: {', '.join(missing)}"}), 400

    session = Session()
    try:
        record = AlgoAnalysis(
            algo            = data["algo"],
            items           = data["items"],
            steps           = data["steps"],
            start_time      = data["start_time"],
            end_time        = data["end_time"],
            total_time_ms   = data["total_time_ms"],
            time_complexity = data["time_complexity"],
            graph_base64    = data["graph_base64"],
        )
        session.add(record)
        session.commit()

        return jsonify({
            "status": "success",
            "id": record.id,
            "message": f"Analysis saved with id {record.id}"
        }), 201
    except Exception as e:
        session.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        session.close()


# ── 3. /retrieve_analysis ────────────────────────────────────────────
@app.route("/retrieve_analysis")
def retrieve_analysis():
    """
    GET /retrieve_analysis?id=1

    Returns the saved analysis row as JSON (same shape as /analyze output).
    """
    analysis_id = request.args.get("id", type=int)
    if analysis_id is None:
        return jsonify({"error": "Missing required query param: id"}), 400

    session = Session()
    try:
        record = session.get(AlgoAnalysis, analysis_id)
        if not record:
            return jsonify({"error": f"No analysis found with id {analysis_id}"}), 404
        return jsonify(record.to_dict()), 200
    finally:
        session.close()


# ── Run ──────────────────────────────────────────────────────────────
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000, debug=True)
