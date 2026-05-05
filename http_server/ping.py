from aiohttp import web
from .validate_token import validate_token

async def ping(request):
    """/ping - возвращает 204 No Content"""
    validate_token(request)
    return web.Response(status=204)