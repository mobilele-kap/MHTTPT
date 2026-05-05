from aiohttp import web
import json
from .validate_token import validate_token

async def disconnect(request):
    """/disconnect - удаляет подключение"""
    validate_token(request)

    try:
        conn_id = request.query.get("connect_id")

        if not isinstance(conn_id, int):
            raise web.HTTPBadRequest(text="conn must be an integer")

        # if conn_id not in connections:
        #     raise web.HTTPNotFound(text=f"Connection {conn_id} not found")

        return web.Response(status=204)

    except json.JSONDecodeError:
        raise web.HTTPBadRequest(text="Invalid JSON body")