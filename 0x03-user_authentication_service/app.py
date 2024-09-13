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

    # Check if the email or password is missing
    if not email or not password:
        abort(400, "Email and password must be provided")

    # Validate the login credentials
    if not AUTH.valid_login(email, password):
        return abort(401, "Invalid credentials")

    # If valid, create a session for the user
    session_id = AUTH.create_session(email)

    # Create a response object and set the session ID as a cookie
    response = make_response(jsonify({"email": email, "message": "logged in"}))
    response.set_cookie("session_id", session_id)

    # Return the response with the session cookie set
    return response


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
