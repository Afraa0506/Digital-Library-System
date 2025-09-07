# backend/utils.py
import re
import os

def validate_email(email: str) -> bool:
    return bool(re.match(r"[^@]+@[^@]+\.[^@]+", email))

def ensure_dir(path: str):
    os.makedirs(path, exist_ok=True)
