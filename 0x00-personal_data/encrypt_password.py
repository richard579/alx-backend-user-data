#!/usr/bin/env python3
"""Returns a salted, hashed password, byte in string"""
import bcrypt


def hash_password(password: str) -> bytes:
    """Returns byte string password"""
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())


def is_valid(hashed_password: bytes, password: str) -> bool:
    """Implement an is_valid to validate that the provided password 
    matches the hashed password."""
    return bcrypt.checkpw(password.encode('utf-8'), hash_password)
