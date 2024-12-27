from robyn import Request

from common.page_info import Page


async def page_handler(request: Request) -> Page:
    page = Page()
    query_params = request.query_params
    try:
        page.page = int(query_params.get("page", '1'))
        page.size = int(query_params.get("size", '20'))
    except ValueError:
        raise ValueError("分页参数错误")
    return page
