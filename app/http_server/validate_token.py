from aiohttp import web

VALID_TOKENS = {"secret", "admin"}

def validate_token(request):
    """Проверяет наличие и валидность токена в заголовке"""
    token = request.headers.get("token")
    if not token or token not in VALID_TOKENS:
        raise web.HTTPUnauthorized(text="Invalid or missing token")
    return token