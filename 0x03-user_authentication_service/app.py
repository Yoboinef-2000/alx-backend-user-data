#!/usr/bin/env python3

"""A Flask Application that has user authentication."""
from flask import Flask, jsonify, request
from auth import Auth

AUTH = Auth()
app = Flask(__name__)


@app.route("/", methods=["GET"])
def welcome():
    """Returns a JSON response with a welcome message."""
    return jsonify({"message": "Bienvenue"})


@app.route("/users", methods=["POST"])
def users():
    """
    POST /users route to register a new user.
    Expects 'email' and 'password' form data.
    Returns a JSON response with either a success or failure message.
    """
    # Get the 'email' and 'password' from the request's form data
    email = request.form.get("email")
    password = request.form.get("password")

    # Check if both email and password are provided
    if not email or not password:
        return jsonify({"message": "Missing email or password"}), 400

    try:
        # Attempt to register the user using Auth
        new_user = AUTH.register_user(email, password)
        # If registration is successful, return a success message
        return jsonify({"email": new_user.email,
                        "message": "user created"}), 201
    except ValueError:
        # If the user already exists, return an error message
        return jsonify({"message": "email already registered"}), 400


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
