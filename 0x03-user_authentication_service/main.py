#!/usr/bin/env python3
"""
Main file for testing user authentication service.
"""
import requests

BASE_URL = "http://localhost:5000"


def register_user(email: str, password: str) -> None:
    """Register a new user with the provided email and password."""
    response = requests.post(
        f"{BASE_URL}/users", data={"email": email, "password": password})
    assert response.status_code == 201
    assert response.json() == {"email": email, "message": "user created"}


def log_in_wrong_password(email: str, password: str) -> None:
    """Try to log in with a wrong password."""
    response = requests.post(
        f"{BASE_URL}/sessions", data={"email": email, "password": password})
    assert response.status_code == 401


def log_in(email: str, password: str) -> str:
    """Log in with the correct credentials and return the session ID."""
    response = requests.post(
        f"{BASE_URL}/sessions", data={"email": email, "password": password})
    assert response.status_code == 200
    session_id = response.cookies.get("session_id")
    assert session_id is not None
    return session_id


def profile_unlogged() -> None:
    """Try to access the profile without being logged in."""
    response = requests.get(f"{BASE_URL}/profile")
    assert response.status_code == 403


def profile_logged(session_id: str) -> None:
    """Access the profile while logged in."""
    cookies = {"session_id": session_id}
    response = requests.get(f"{BASE_URL}/profile", cookies=cookies)
    assert response.status_code == 200
    assert "email" in response.json()


def log_out(session_id: str) -> None:
    """Log out a user by ending the session."""
    cookies = {"session_id": session_id}
    response = requests.delete(f"{BASE_URL}/sessions", cookies=cookies)
    assert response.status_code == 200


def reset_password_token(email: str) -> str:
    """Get a reset password token for the given email."""
    response = requests.post(
        f"{BASE_URL}/reset_password", data={"email": email})
    assert response.status_code == 200
    reset_token = response.json().get("reset_token")
    assert reset_token is not None
    return reset_token


def update_password(email: str, reset_token: str, new_password: str) -> None:
    """Update the password with the reset token and new password."""
    response = requests.put(
        f"{BASE_URL}/reset_password", data={"email": email,
                                            "reset_token": reset_token,
                                            "new_password": new_password})
    assert response.status_code == 200
    assert response.json() == {"email": email, "message": "Password updated"}


# Example data
EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"

if __name__ == "__main__":
    register_user(EMAIL, PASSWD)
    log_in_wrong_password(EMAIL, NEW_PASSWD)
    profile_unlogged()
    session_id = log_in(EMAIL, PASSWD)
    profile_logged(session_id)
    log_out(session_id)
    reset_token = reset_password_token(EMAIL)
    update_password(EMAIL, reset_token, NEW_PASSWD)
    log_in(EMAIL, NEW_PASSWD)
