import json
import threading
from abc import ABC
from typing import Optional
from urllib.request import Request

from robyn import AuthenticationHandler
from robyn.authentication import BearerGetter
from robyn.robyn import Identity, Response, Headers
from robyn.status_codes import HTTP_401_UNAUTHORIZED

from common.cjwt import decode_token


class AuthenticationMiddleware(AuthenticationHandler, ABC):
    def __init__(self):
        self.token_getter = BearerGetter()
        self.local_context = threading.local()

    def authenticate(self, request: Request) -> Optional[Identity]:
        try:
            token = self.token_getter.get_token(request)
            if not token:
                raise ValueError("Missing token")
            payload = decode_token(token)
            if "error" in payload:
                raise ValueError(payload["error"])
            user_id = payload.get("user_id")
            username = payload.get("username")
            user_data = {
                "user_id": user_id,
                "username": username,
            }
            claims = json.dumps(user_data)
            return Identity({"claims": claims})
        except (IndexError, ValueError) as e:
            self.local_context.auth_error = str(e)
            return None

    @property
    def unauthorized_response(self) -> Response:
        error_message = getattr(self.local_context, "auth_error", "Unauthorized access")
        return Response(
            headers=Headers({
                "WWW-Authenticate": self.token_getter.scheme,
                "content-type": "application/json",
            }),
            description=json.dumps({
                "code": HTTP_401_UNAUTHORIZED,
                "message": error_message,
            }),
            status_code=HTTP_401_UNAUTHORIZED,
        )
