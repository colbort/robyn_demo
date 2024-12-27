import datetime

import jwt

# 秘钥和算法
SECRET_KEY = "ZsdFT0rlf8RhPr4jMgzftMbz-QDzDzR58JXVDUEYWXc"
ALGORITHM = "HS256"


# 生成 JWT Token
def create_token(user_id, username):
    now = datetime.datetime.utcnow()
    payload = {
        "user_id": user_id,
        "username": username,
        "exp": now + datetime.timedelta(days=7),
        "iat": now,  # 签发时间
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return token


# 解码 JWT Token
def decode_token(token):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        return {"error": "Token expired"}
    except jwt.InvalidTokenError:
        return {"error": "Invalid token"}
