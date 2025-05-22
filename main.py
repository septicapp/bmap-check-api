
from flask import Flask, request, jsonify
import requests
from shapely.geometry import shape, Point

app = Flask(__name__)

GEOJSON_URL = "https://raw.githubusercontent.com/septicapp/bmap-data/main/bmap_zones.geojson"

@app.route("/check-bmap", methods=["POST"])
def check_bmap():
    data = request.get_json()
    lat = float(data.get("lat"))
    lng = float(data.get("lng"))

    if lat is None or lng is None:
        return jsonify({"error": "Missing lat or lng"}), 400

    point = Point(lng, lat)
    response = requests.get(GEOJSON_URL)
    geojson = response.json()

    for feature in geojson["features"]:
        polygon = shape(feature["geometry"])
        if polygon.contains(point):
            return jsonify({"insideBMAP": True})

    return jsonify({"insideBMAP": False})

# 🟡 REQUIRED to run in production
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)