#!/usr/bin/env python3
"""
The authentication module.
"""
from flask import request
from typing import List, TypeVar


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

        if path in excluded_paths:
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
