# win_ram_api.py
import psutil
from flask import Flask, jsonify

app = Flask(__name__)

@app.get("/ram")
def ram():
    mem = psutil.virtual_memory()
    total_gb = mem.total / 1024**3
    used_gb = mem.used / 1024**3
    free_gb = mem.available / 1024**3

    return jsonify({
        "total_gb": round(total_gb, 2),
        "used_gb": round(used_gb, 2),
        "free_gb": round(free_gb, 2)
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5055)
