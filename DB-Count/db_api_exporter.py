from flask import Flask, Response
import requests

app = Flask(__name__)

API_URL = "https://api.auctionindia.com/utility-crud/api/v1/database-health"

@app.route("/metrics")
def metrics():
    try:
        r = requests.get(API_URL, timeout=5)
        r.raise_for_status()          # ❗ raises exception on 4xx / 5xx
        payload = r.json()
    except Exception as e:
        # IMPORTANT:
        # - Return 200
        # - Empty body
        # Prometheus treats this as "no data", not "scrape failed"
        return Response("", mimetype="text/plain")

    data = payload.get("Data", [])
    output = []

    for db in data:
        name = db.get("DatabaseName")
        active = db.get("ActiveConnections")

        if name is not None and active is not None:
            output.append(
                f'db_active_connections{{database="{name}"}} {active}'
            )

    return Response("\n".join(output) + "\n", mimetype="text/plain")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=9105)
