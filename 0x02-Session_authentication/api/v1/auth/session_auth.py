#!/usr/bin/env python3
""" SessionAuth module
"""
from api.v1.auth.auth import Auth
from models.user import User
import uuid


class SessionAuth(Auth):
    """ SessionAuth class that handles session-based authentication """

    # Class attribute to store user_id by session_id
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """
        Creates a session ID for the given user_id.

        Args:
            user_id (str): The ID of the user for whom to create the session.

        Returns:
            str: The created session ID, or None if user_id is invalid.
        """
        if user_id is None or not isinstance(user_id, str):
            return None

        # Generate a unique session ID using uuid4()
        session_id = str(uuid.uuid4())

        # Store the session ID with the user_id in the dictionary
        SessionAuth.user_id_by_session_id[session_id] = user_id

        # Return the session ID
        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """
        Retrieves the user ID associated with a session ID.

        Args:
            session_id (str): The session ID.

        Returns:
            str: The user ID associated with the session ID, or None if invalid
        """
        if session_id is None or not isinstance(session_id, str):
            return None

        # Retrieve the user ID for the session ID from the dictionary
        return SessionAuth.user_id_by_session_id.get(session_id)

    def current_user(self, request=None):
        """
        Returns a User instance based on a cookie value.
        """
        session_id = self.session_cookie(request)
        if session_id is None:
            return None

        user_id = self.user_id_for_session_id(session_id)
        if user_id is None:
            return None

        try:
            # Retrieve the user from the database based on the user_id
            user = User.get(user_id)
        except Exception:
            return None

        return user

    def destroy_session(self, request=None):
        """
        Deletes the user session / logs out the user.

        Args:
            request (flask.Request): The request object containing
            the session cookie.

        Returns:
            bool: True if the session was successfully deleted, False otherwise
        """
        if request is None:
            return False

        # Get the session ID from the cookie
        session_id = self.session_cookie(request)
        if session_id is None:
            return False

        # Check if the session ID is linked to a user ID
        if self.user_id_for_session_id(session_id) is None:
            return False

        # Delete the session ID from the user_id_by_session_id dictionary
        del self.user_id_by_session_id[session_id]
        return True
