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
