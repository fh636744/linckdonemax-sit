from flask import Flask, request, jsonify
import os
import hmac

app = Flask(__name__)

API_KEY = os.environ.get("rnd_JW6da5IO6jCgpU3jJGPNBrjzOUQk", "CHANGE_THIS_SECRET")
auto_reply_enabled = False


def authorized():
    key = request.headers.get("X-API-Key", "")
    return hmac.compare_digest(key, API_KEY)


@app.route("/")
def home():
    return jsonify({
        "ok": True,
        "message": "Python API is running"
    })


@app.route("/status")
def status():
    if not authorized():
        return jsonify({"ok": False, "error": "Unauthorized"}), 401

    return jsonify({
        "ok": True,
        "enabled": auto_reply_enabled
    })


@app.route("/toggle", methods=["POST"])
def toggle():
    global auto_reply_enabled

    if not authorized():
        return jsonify({"ok": False, "error": "Unauthorized"}), 401

    data = request.get_json(silent=True) or {}
    enabled = data.get("enabled")

    if not isinstance(enabled, bool):
        return jsonify({
            "ok": False,
            "error": "enabled must be true or false"
        }), 400

    auto_reply_enabled = enabled

    return jsonify({
        "ok": True,
        "enabled": auto_reply_enabled
    })
