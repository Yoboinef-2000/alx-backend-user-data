#!/usr/bin/env python3

"""A Flask Application that has user authentication."""
from flask import Flask, jsonify
from auth import Auth

app = Flask(__name__)


@app.route("/", methods=["GET"])
def welcome():
    """Returns a JSON response with a welcome message."""
    return jsonify({"message": "Bienvenue"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
