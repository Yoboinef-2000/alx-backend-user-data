#!/usr/bin/env python3

"""Encrypting passwords."""
import bcrypt


def hash_password(password: str) -> bytes:
    """
    Hash a password using bcrypt, with automatic salting.

    Args:
        password (str): The password to hash.

    Returns:
        bytes: The salted, hashed password as a byte string.
    """
    # Generate a salt and hash the password with bcrypt
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode(), salt)

    return hashed_password


def is_valid(hashed_password: bytes, password: str) -> bool:
    """
    Validate that the provided password matches the hashed password.

    Args:
        hashed_password (bytes): The hashed password to check against.
        password (str): The plain text password to validate.

    Returns:
        bool: True if the password matches the hashed password, False otherwise
    """
    return bcrypt.checkpw(password.encode(), hashed_password)
