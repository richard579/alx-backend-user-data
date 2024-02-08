#!/usr/bin/env python3
"""Returns a salted, hashed password, byte in string"""
import bcrypt


def hash_password(password: str) -> bytes:
    """Returns byte string password"""
    encoded = password.encode()
    hashed = bcrypt.hashpw(encoded, bcrypt.gensalt())
    return hashed


def is_valid(hashed_password: bytes, password: str) -> bool:
    """Implement an is_valid to validate that the provided password 
    matches the hashed password."""
    valid = False
    encoded = password.encode()
    if bcrypt.checkpw(encoded, hashed_password):
        valid = True
    return valid
