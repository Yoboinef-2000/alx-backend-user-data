#!/usr/bin/env python3
"""The Auth Module.
"""

import bcrypt
from db import DB
from sqlalchemy.orm.exc import NoResultFound
from user import User
import uuid
from typing import Union


def _hash_password(password: str) -> str:
    """
    Hashes a password using bcrypt with automatic salting.

    Args:
        password (str): The plain text password to be hashed.

    Returns:
        bytes: The salted and hashed password.
    """
    # Generate a salt
    salt = bcrypt.gensalt()

    # Hash the password with the salt
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)

    return hashed_password


def _generate_uuid() -> str:
    """
    Generate a new UUID and return its string representation.

    Returns:
        str: A string representation of a new UUID.
    """
    return str(uuid.uuid4())


class Auth:
    """Auth class to interact with the authentication database."""

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """Register a new user with email and hashed password."""
        try:
            # Check if a user with the given email already exists
            self._db.find_user_by(email=email)
            raise ValueError(f"User {email} already exists")
        except NoResultFound:
            # If the user does not exist, hash the password
            hashed_password = self._hash_password(password)

            # Add the user to the database
            new_user = self._db.add_user(email, hashed_password)

            # Return the created User object
            return new_user

    def valid_login(self, email: str, password: str) -> bool:
        """
        Validate login by checking email and password.
        Args:
            email (str): The email of the user.
            password (str): The plain text password to verify.
        Returns:
            bool: True if login is valid, False otherwise.
        """
        user = None
        try:
            user = self._db.find_user_by(email=email)
            if user is not None:
                return bcrypt.checkpw(
                    password.encode("utf-8"),
                    user.hashed_password,
                )
        except NoResultFound:
            return False
        return False

    def create_session(self, email: str) -> str:
        """
        Create a new session for a user with the given email.
        Args:
            email (str): The email of the user.
        Returns:
            str: The session ID if the user exists, otherwise None.
        """
        try:
            user = self._db.find_user_by(email=email)
        except Exception:
            return None
        session_id = _generate_uuid()
        self._db.update_user(user.id, session_id=session_id)
        return session_id
    
    def get_user_from_session_id(self, session_id: str) -> Union[User, None]:
        """User Retriever.
        """
        user = None
        if session_id is None:
            return None
        try:
            user = self._db.find_user_by(session_id=session_id)
        except NoResultFound:
            return None
        return user

    def destroy_session(self, user_id: int) -> None:
        """Session Destroyer.
        """
        if user_id is None:
            return None
        self._db.update_user(user_id, session_id=None)

    def get_reset_password_token(self, email: str) -> str:
        """Reset password generator.
        """
        user = None
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            user = None
        if user is None:
            raise ValueError()
        reset_token = _generate_uuid()
        self._db.update_user(user.id, reset_token=reset_token)
        return reset_token

    def update_password(self, reset_token: str, password: str) -> None:
        """Updates a user's password given the user's reset token.
        """
        user = None
        try:
            user = self._db.find_user_by(reset_token=reset_token)
        except NoResultFound:
            user = None
        if user is None:
            raise ValueError()
        new_password_hash = _hash_password(password)
        self._db.update_user(
            user.id,
            hashed_password=new_password_hash,
            reset_token=None,
        )
