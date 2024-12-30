from pydantic_core import ValidationError
from robyn import Robyn, Request

from common.cjwt import create_token
from common.identify_parse import get_user_id
from common.response import fail, success, error
from common.router_group import RouterGroup
from handler.translator_handler import Translator
from service_user.request.req_login import ReqLogin
from service_user.request.req_register import ReqRegister
from service_user.services.user_service import *


class UserController:
    def __init__(self, app: Robyn):
        self.app = RouterGroup(app, "/api/v1/user/")
        self._setup_routes()

    def _setup_routes(self):
        @self.app.post("register")
        async def _register(request: Request):
            try:
                data = ReqRegister(**request.json())
                user_id, username = await register_user(data.email, data.phone_country_code, data.phone, data.password)
                if not user_id or not username:
                    return fail(message="创建用户失败")
                else:
                    return success(data={"token": create_token(user_id, username)})
            except ValidationError as e:
                return fail(code=400, message=f"参数验证失败 {e.errors()}")
            except Exception as e:
                logger.error(f'用户注册失败 {e}')
                import traceback
                logger.error(traceback.format_exc())
                return error(message=f"用户注册失败; {e}")

        @self.app.post("login", language="language")
        async def _login(request: Request, language: str):
            try:
                logger.info(f"Detected language: {language} ")
                data = ReqLogin(**request.json())
                user_id, username = await login_user(
                    email=data.email,
                    phone_country_code=data.phone_country_code,
                    phone=data.phone,
                    username=data.username,
                    password=data.password,
                )
                logger.info(Translator.get_translation("1001001", language))
                logger.info(Translator.get_translation("1001002", language))
                if not user_id or not username:
                    return fail(message="登录失败")
                else:
                    return success(data={"token": create_token(user_id, username)})
            except ValidationError as e:
                return fail(code=400, message=f"参数验证失败 {e.errors()}")
            except Exception as e:
                logger.error(f'登录失败 {e}')
                import traceback
                logger.error(traceback.format_exc())
                return error(message=f"登录失败; {e}")

        @self.app.post("logout", auth_required=True)
        async def _logout(request: Request):
            try:
                user_id = get_user_id(request.identity)
            except Exception as e:
                logger.error(f'退出登录失败 {e}')
                import traceback
                logger.error(traceback.format_exc())
                return error(message=f"退出登录失败; {e}")

        @self.app.get("info", auth_required=True)
        async def _get_user(request: Request):
            try:
                user_id = get_user_id(request.identity)
                user = await get_user_info(user_id)
                if user:
                    return success(data={
                        "user_id": user.id,
                        "username": user.username,
                        "nickname": user.nickname,
                        "avatar": user.avatar,
                        "balance": user.balance,
                        "frozen_amount": user.frozen_amount,
                        "phone_country_code": user.phone_country_code,
                        "phone": user.phone,
                        "email": user.email,
                    })
                else:
                    return fail(message="用户不存在")
            except Exception as e:
                logger.error(f'获取用户信息失败 {e}')
                import traceback
                logger.error(traceback.format_exc())
                return error(message=f"获取用户信息失败; {e}")

        @self.app.post("update", auth_required=True)
        async def _update(request: Request):
            """
            更新用户信息
            :param request:
            :return:
            """
            try:
                user_id = get_user_id(request.identity)
                data = ReqUpdate(**request.json())
                if await update_user_info(user_id, data):
                    return success(message="修改用户信息成功")
                else:
                    return fail(message="更新用户信息失败")
            except Exception as e:
                logger.error(f'更新用户信息失败 {e}')
                import traceback
                logger.error(traceback.format_exc())
                return error(message=f"更新用户信息失败 {e}")
