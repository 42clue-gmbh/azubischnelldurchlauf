import time
import math
from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/temperatur', methods=["GET"])
def temperatur():
    response = {
        "computer": abs(math.tan(time.time())) + 40,
        "draussen": abs(math.sin(time.time() * 0.01) * 25),
        "drinnen": abs(math.cos(time.time() * 0.01) * 10) + 15
    }
    return jsonify(response)

if __name__ == "__main__":
    app.run(debug=True)
