from typing import Optional

from robyn import Robyn, Request


class RouterGroup:
    """路由分组类"""

    def __init__(self, app: Robyn, prefix: str):
        self.app = app
        self.prefix = prefix
        self.dependencies = app.dependencies

    async def _resolve_dependency(self, request: Request, language: Optional[str] = None):
        """解析依赖"""
        if language:
            dependency = self.dependencies.global_dependency_map.get(language)
            if dependency:
                return await dependency(request)
        return None

    async def _parse_pagination(self, request: Request, pagination: Optional[str] = None):
        """解析分页参数并绑定到 request"""
        if pagination:
            dependency = self.dependencies.global_dependency_map.get(pagination)
            if dependency:
                return await dependency(request)
        return None

    def _wrap_handler(self, handler, language: Optional[str] = None, pagination: Optional[str] = None):
        """包装处理程序以支持动态依赖注入"""

        async def wrapped_handler(request: Request):
            # 动态获取语言依赖
            language_value = None
            if language:
                language_value = await self._resolve_dependency(request, language)

            # 动态获取分页参数
            page_value = None
            if pagination:
                page_value = await self._parse_pagination(request, pagination)

            # 获取处理函数参数列表
            handler_params = handler.__code__.co_varnames[:handler.__code__.co_argcount]

            # 根据处理函数定义的参数数量动态传参
            if len(handler_params) == 1:
                return await handler(request)
            elif len(handler_params) == 2:
                if language and page_value:
                    raise TypeError(f"Handler {handler.__name__} 参数定义错误，不能同时注入 language 和分页参数")
                if language_value:
                    return await handler(request, language_value)
                if page_value:
                    return await handler(request, page_value)
            elif len(handler_params) == 3:
                if language_value and page_value:
                    return await handler(request, language_value, page_value)
                raise TypeError(f"Handler {handler.__name__} 参数定义错误，language 和分页参数必须同时定义")
            else:
                raise TypeError(f"Handler {handler.__name__} 参数定义错误，无法注入依赖")

        return wrapped_handler

    def get(
            self,
            endpoint: str,
            const: bool = False,
            auth_required: bool = False,
            language: Optional[str] = None,
            pagination: Optional[str] = None
    ):
        """GET 请求装饰器"""

        def decorator(handler):
            wrapped_handler = self._wrap_handler(handler, language, pagination)
            self.app.get(f"{self.prefix}{endpoint}", const, auth_required)(wrapped_handler)
            return handler

        return decorator

    def post(
            self,
            endpoint: str,
            auth_required: bool = False,
            language: Optional[str] = None,
            pagination: Optional[str] = None
    ):
        """POST 请求装饰器"""

        def decorator(handler):
            wrapped_handler = self._wrap_handler(handler, language, pagination)
            self.app.post(f"{self.prefix}{endpoint}", auth_required)(wrapped_handler)
            return handler

        return decorator
