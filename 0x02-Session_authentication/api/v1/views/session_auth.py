#!/usr/bin/env python3
"""
Session authentication routes
"""
from flask import jsonify, request, abort
from models.user import User
from os import getenv

from api.v1.views import app_views


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def session_auth_login():
    """
    Handles user login via session authentication.
    """
    email = request.form.get('email')
    password = request.form.get('password')

    # Check if email is missing
    if not email:
        return jsonify({"error": "email missing"}), 400

    # Check if password is missing
    if not password:
        return jsonify({"error": "password missing"}), 400

    # Retrieve the User instance based on the email
    try:
        users = User.search({'email': email})
    except Exception:
        return jsonify({"error": "no user found for this email"}), 404

    if len(users) == 0:
        return jsonify({"error": "no user found for this email"}), 404

    user = users[0]

    # Validate the password
    if not user.is_valid_password(password):
        return jsonify({"error": "wrong password"}), 401

    # Importing `auth` from api.v1.app here to avoid circular imports
    from api.v1.app import auth

    # Create a session ID for the user
    session_id = auth.create_session(user.id)
    if session_id is None:
        abort(500)

    # Create the response containing the user's JSON representation
    response = jsonify(user.to_json())

    # Set the session ID cookie in the response
    session_name = getenv('SESSION_NAME')
    response.set_cookie(session_name, session_id)

    return response
