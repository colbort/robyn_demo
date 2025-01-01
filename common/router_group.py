from typing import Optional

from robyn import Robyn, Request

from middleware.rate_limit_middleware import RateLimitMiddleware


class RouterGroup:
    """路由分组类"""

    def __init__(self, app: Robyn, prefix: str):
        self.app = app
        self.prefix = prefix
        self.dependencies = app.dependencies
        self.rate_limit_dependency = RateLimitMiddleware()  # 初始化限流依赖

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

    async def _apply_rate_limiting(self, request: Request):
        """应用限流检查"""
        rate_limit_response = await self.rate_limit_dependency(request)
        if rate_limit_response:
            # 如果限流响应不为空，返回限流错误
            return rate_limit_response
        return None

    def _wrap_handler(self, handler, language: Optional[str] = None, page: Optional[str] = None):
        """包装处理程序以支持动态依赖注入"""

        async def wrapped_handler(request: Request):
            # 先执行限流
            rate_limit_response = await self._apply_rate_limiting(request)
            if rate_limit_response:
                return rate_limit_response  # 如果限流拒绝请求，直接返回限流响应

            # 动态获取语言依赖
            language_value = None
            if language:
                language_value = await self._resolve_dependency(request, language)

            # 动态获取分页参数
            page_value = None
            if page:
                page_value = await self._parse_pagination(request, page)

            # 获取处理函数参数列表
            handler_params = handler.__code__.co_varnames[:handler.__code__.co_argcount]

            # 动态注入依赖
            args = []
            for param in handler_params:
                if param == "request":
                    args.append(request)
                elif param == "language" and language_value:
                    args.append(language_value)
                elif param == "page" and page_value:
                    args.append(page_value)

            if len(args) != len(handler_params):
                raise TypeError(f"Handler {handler.__name__} 参数定义错误，无法注入依赖")

                # 执行处理程序
            return await handler(*args)

        return wrapped_handler

    def get(
            self,
            endpoint: str,
            const: bool = False,
            auth_required: bool = False,
            language: Optional[str] = None,
            page: Optional[str] = None
    ):
        """GET 请求装饰器"""

        def decorator(handler):
            wrapped_handler = self._wrap_handler(handler, language, page)
            self.app.get(f"{self.prefix}{endpoint}", const, auth_required)(wrapped_handler)
            return handler

        return decorator

    def post(
            self,
            endpoint: str,
            auth_required: bool = False,
            language: Optional[str] = None,
            page: Optional[str] = None
    ):
        """POST 请求装饰器"""

        def decorator(handler):
            wrapped_handler = self._wrap_handler(handler, language, page)
            self.app.post(f"{self.prefix}{endpoint}", auth_required)(wrapped_handler)
            return handler

        return decorator
