#!/usr/bin/env python3
""" SessionAuth module
"""
from api.v1.auth.auth import Auth
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
