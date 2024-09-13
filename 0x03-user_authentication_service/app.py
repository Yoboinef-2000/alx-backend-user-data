#!/usr/bin/env python3

"""A Flask Application that has user authentication."""
from flask import Flask, jsonify, \
    request, abort, redirect, make_response
from auth import Auth


app = Flask(__name__)
AUTH = Auth()


@app.route("/", methods=["GET"])
def welcome():
    """Returns a JSON response with a welcome message."""
    return jsonify({"message": "Bienvenue"})


@app.route("/sessions", methods=["POST"])
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

    # If either email or password is missing, abort with a 401 error
    if not email or not password:
        abort(401)

    # Validate the login credentials using Auth.valid_login
    if not AUTH.valid_login(email, password):
        abort(401)

    # If valid, create a session for the user
    session_id = AUTH.create_session(email)

    # If session creation fails, abort with a 401
    # error (this is optional based on your implementation)
    if not session_id:
        abort(401)

    # Create a response object with JSON data
    response = make_response(jsonify({"email": email, "message": "logged in"}))

    # Set the session ID as a cookie in the response
    response.set_cookie("session_id", session_id)

    # Return the response with the session cookie set
    return response


@app.route("/reset_password", methods=["PUT"])
def update_password():
    """
    Update the user's password after verifying the reset token.
    Responds to the PUT /reset_password route.
    Expects form data with 'email', 'reset_token', and 'new_password'.
    """
    # Get the form data from the request
    email = request.form.get("email")
    reset_token = request.form.get("reset_token")
    new_password = request.form.get("new_password")

    # Check if any of the required fields are missing
    if not email or not reset_token or not new_password:
        abort(400, "Missing email, reset token, or new password")

    try:
        # Attempt to update the user's password using the Auth service
        AUTH.update_password(email, reset_token, new_password)

        # If successful, return a JSON response with a 200 status code
        return jsonify({"email": email, "message": "Password updated"}), 200

    except ValueError:
        # If the reset token is invalid, respond with a 403 status code
        return jsonify({"message": "Invalid reset token"}), 403


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
