from robyn import Request


async def i18n_handler(request: Request) -> str:
    lang = request.headers.get("Accept-Language")
    if not lang:
        lang = 'en'
    if "lang" in request.query_params:
        lang = request.query_params.get("lang", "en")
    return lang
