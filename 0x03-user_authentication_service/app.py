#!/usr/bin/env python3

"""A Flask Application that has user authentication."""
from flask import Flask, jsonify, \
    request, abort, redirect, make_response
from auth import Auth


app = Flask(__name__)
AUTH = Auth()


@app.route("/", methods=["GET"], strict_slashes=False)
def welcome():
    """Returns a JSON response with a welcome message."""
    return jsonify({"message": "Bienvenue"})


@app.route("/sessions", methods=["POST"], strict_slashes=False)
def login():
    """
    POST /sessions route to handle user login.
    Expects 'email' and 'password' in form data.
    If the login is successful, a session is created,
    and the session ID is stored as a cookie.
    If the login fails, it returns a 401 error.
    """
    # Get the 'email' and 'password' from the request's form data
    email = request.form.get("email")
    password = request.form.get("password")

    try:
        AUTH.register_user(email, password)
        return jsonify({"email": email, "message": "user created"})

    except ValueError:
        return jsonify({"message": "email already registered"}), 400


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
