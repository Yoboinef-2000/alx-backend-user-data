#!/usr/bin/env python3
"""
BasicAuth module for the API.
"""
from api.v1.auth.auth import Auth
import base64
from models.user import User
from typing import TypeVar


class BasicAuth(Auth):
    """BasicAuth class for handling basic authentication"""
    def extract_base64_authorization_header(self,
                                            authorization_header: str) -> str:
        """
        Extracts the Base64 part of the Authorization header
        for Basic Authentication.

        Args:
            authorization_header (str):
            The Authorization header.

        Returns:
            str: The Base64 part of the header,
            or None if the header is invalid.
        """
        if authorization_header is None:
            return None

        if not isinstance(authorization_header, str):
            return None

        if not authorization_header.startswith('Basic '):
            return None

        # Extract and return the Base64 part of the header (after 'Basic ')
        return authorization_header[len('Basic '):]

    def decode_base64_authorization_header(
            self, base64_authorization_header: str) -> str:
        """
        Decodes the Base64 string to a regular string.

        Args:
            base64_authorization_header (str): The Base64
            string to decode.

        Returns:
            str: The decoded value as a UTF-8 string,
            or None if decoding fails.
        """
        if base64_authorization_header is None:
            return None

        if not isinstance(base64_authorization_header, str):
            return None

        try:
            # Decode the Base64 string
            decoded_bytes = base64.b64decode(base64_authorization_header)
            # Convert the bytes to a UTF-8 string
            return decoded_bytes.decode('utf-8')
        except Exception:
            # If decoding fails, return None
            return None

    def extract_user_credentials(
            self, decoded_base64_authorization_header: str) -> (str, str):
        """
        Extracts the user email and password
        from the Base64 decoded value.

        Args:
            decoded_base64_authorization_header (str):
            The decoded Base64 string.

        Returns:
            tuple: A tuple containing the user email and
            password, or (None, None) if invalid.
        """
        if decoded_base64_authorization_header is None:
            return None, None

        if not isinstance(decoded_base64_authorization_header, str):
            return None, None

        if ':' not in decoded_base64_authorization_header:
            return None, None

        user_email, user_password = \
            decoded_base64_authorization_header.split(':', 1)
        return user_email, user_password

    def user_object_from_credentials(
            self, user_email: str, user_pwd: str) -> TypeVar('User'):
        """
        Retrieves the User instance based on the provided email and password.

        Args:
            user_email (str): The user's email.
            user_pwd (str): The user's password.

        Returns:
            User: The User instance if credentials are valid, otherwise None.
        """
        if user_email is None or not isinstance(user_email, str):
            return None

        if user_pwd is None or not isinstance(user_pwd, str):
            return None

        # Search for the user with the provided email
        users = User.search({"email": user_email})

        if not users:
            return None

        user = users[0]  # Assuming email is unique, get the first match

        # Validate the password
        if not user.is_valid_password(user_pwd):
            return None

        return user
