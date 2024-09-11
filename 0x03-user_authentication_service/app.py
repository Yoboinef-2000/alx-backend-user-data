#!/usr/bin/env python3

"""A Flask Application that has user authentication."""
from flask import Flask, jsonify, request
from auth import Auth


app = Flask(__name__)

AUTH = Auth()


@app.route("/", methods=["GET"])
def welcome():
    """Returns a JSON response with a welcome message."""
    return jsonify({"message": "Bienvenue"})


@app.route("/users", methods=["POST"])
def users():
    """
    POST /users route to register a new user.
    Expects 'email' and 'password' form data.
    """
    # Get the email and password from form data
    email = request.form.get("email")
    password = request.form.get("password")

    # If email or password is missing, return a 400 error
    if not email or not password:
        return jsonify({"message": "Missing email or password"}), 400

    try:
        # Try to register the user using AUTH.register_user
        user = AUTH.register_user(email, password)
        # If successful, return a success message
        return jsonify({"email": user.email, "message": "user created"})
    except ValueError:
        # If the email is already registered, return an error message
        return jsonify({"message": "email already registered"}), 400


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
