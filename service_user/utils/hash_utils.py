import hashlib
import time


def hash_password(password: str, salt: str) -> str:
    return hashlib.sha256((password + salt).encode()).hexdigest()


def verify_password(password: str, salt: str, hashed_password: str) -> bool:
    return hash_password(password, salt) == hashed_password


def generate_unique_username():
    timestamp = str(time.time()).encode('utf-8')
    hash_object = hashlib.md5(timestamp)
    return hash_object.hexdigest()[:11]
