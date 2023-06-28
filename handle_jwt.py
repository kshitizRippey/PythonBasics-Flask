import os
import time
import jwt
from dotenv import load_dotenv

load_dotenv()
SECRET = os.getenv("SECRET")
ALGORITHM = os.getenv("ALGORITHM")


def sign_jwt(username: str) -> str:
    payload = {
        "username": username,
        "expiry": time.time() + 3600
    }
    token = jwt.encode(payload, SECRET, ALGORITHM)
    return token


def decode_jwt(token: str) -> dict:
    try:
        decode_token = jwt.decode(token, SECRET, ALGORITHM)
        if decode_token["expiry"] >= time.time():
            return decode_token
    except:
        return {}


def is_logged_in(token: str) -> bool:
    payload = decode_jwt(token)
    return True if payload else False


def get_user_name(token: str) -> str:
    payload = decode_jwt(token)
    return payload.get("username")
