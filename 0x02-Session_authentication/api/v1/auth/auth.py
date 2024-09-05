#!/usr/bin/env python3
"""
The authentication module.
"""
from flask import request
from typing import List, TypeVar
from os import getenv


class Auth:
    """Class Auth."""

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """require_auth method: that was helpful wasnt it?"""
        if path is None:
            return True

        if not excluded_paths or len(excluded_paths) == 0:
            return True

        if not path.endswith('/'):
            path += '/'

        # if path in excluded_paths:
        #     return False
        for excluded_path in excluded_paths:
            # If the excluded path ends with a wildcard '*',
            # check for prefix match
            if excluded_path.endswith('*'):
                prefix = excluded_path[:-1]  # Remove the '*' to get the prefix
                if path.startswith(prefix):
                    return False
            elif excluded_path == path:
                return False

        return True

    def authorization_header(self, request=None) -> str:
        """authorization_header method: that was helpful wasnt it?"""
        if request is None:
            return None
        if 'Authorization' not in request.headers:
            return None
        return request.headers.get('Authorization')

    def current_user(self, request=None) -> TypeVar('User'):
        """current_user method: that was helpful wasnt it?"""
        return None

    def session_cookie(self, request=None):
        """
        Retrieves the session cookie value from the request.

        Args:
            request: The Flask request object.

        Returns:
            The value of the session cookie or None if not found.
        """
        if request is None:
            return None

        # Retrieve the session name from the environment variable
        session_name = getenv('SESSION_NAME')

        if session_name is None:
            return None

        # Return the session cookie value if present
        return request.cookies.get(session_name)
