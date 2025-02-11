import datetime

import jwt

from common import aes
from config import config as config

# 算法
ALGORITHM = "HS256"


# 生成 JWT Token
def create_token(user_id: int, username: str, password: str, extend: str):
    now = datetime.datetime.utcnow()
    payload = {
        "user_id": user_id,
        "username": username,
        "exp": now + datetime.timedelta(days=7),
        "iat": now,  # 签发时间
        "extend": aes.encrypt(extend, password[0:32])
    }
    token = jwt.encode(payload, config.Token.secret_key(), algorithm=ALGORITHM)
    return token


# 解码 JWT Token
def decode_token(token):
    try:
        payload = jwt.decode(token, config.Token.secret_key(), algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        return {"error": "Token expired"}
    except jwt.InvalidTokenError:
        return {"error": "Invalid token"}
