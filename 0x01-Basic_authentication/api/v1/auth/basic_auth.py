#!/usr/bin/env python3
"""
BasicAuth module for the API.
"""
from api.v1.auth.auth import Auth
import base64


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
