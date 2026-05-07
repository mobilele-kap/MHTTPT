from aiohttp import web
import json
from .validate_token import validate_token

async def connect(request):
    """/connect - создает новое подключение"""
    validate_token(request)

    try:
        host = request.query.get("host")
        port = request.query.get("port")

        # Валидация параметров
        if not isinstance(host, str) or not host:
            raise web.HTTPBadRequest(text="host must be a non-empty string")

        if not isinstance(port, int) or not (10 <= port <= 65534):
            raise web.HTTPBadRequest(text="port must be an integer between 10 and 65534")

        # Генерация ID нового подключения


        return web.json_response({"connect_id": 1})

    except json.JSONDecodeError:
        raise web.HTTPBadRequest(text="Invalid JSON body")