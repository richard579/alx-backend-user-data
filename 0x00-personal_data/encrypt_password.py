#!/usr/bin/env python3
"""
Returns the log message obfuscated
"""
import bcrypt


def hash_password(password: str) -> bytes:
    """Hash password using bcrypt package
    to perform the hashing with hashpw
    """
    # Convert password to bytes
    byte_pass = password.encode('utf-8')
    # Generate salt to add to password
    gen_salt = bcrypt.gensalt()

    hash_pass = bcrypt.hashpw(byte_pass, gen_salt)
    return hash_pass


def is_valid(hashed_password: bytes, password: str) -> bool:
    """Validate that the provided password
    matches the hashed password
    """
    # Convert password to bytes
    bytes_pass = password.encode('utf-8')
    is_val = bcrypt.checkpw(bytes_pass, hashed_password)
    return is_val
