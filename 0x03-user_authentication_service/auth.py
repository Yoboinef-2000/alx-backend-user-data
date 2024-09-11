#!/usr/bin/env python3

import bcrypt


def _hash_password(password: str) -> bytes:
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
