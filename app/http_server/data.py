from aiohttp import web
import json
from .validate_token import validate_token

async def data(request):
    """/d - обрабатывает данные"""

    validate_token(request)

    try:
        # Параметр conn может быть в query string или в JSON
        connect_id = None
        tx_data = None

        conn_param = request.query.get("c")
        if conn_param:
            try:
                connect_id = int(conn_param)
            except ValueError:
                raise web.HTTPBadRequest(text="c (connect_id) must be an integer")

        # Парсим body
        body = await request.json()

        tx_data = body.get("tx")
        if not isinstance(tx_data, list):
            raise web.HTTPBadRequest(text="tx must be a list")

        # Проверяем существование подключения
        # raise web.HTTPNotFound(text=f"Connection {conn_id} not found")

        # Формируем ответ (пример: транслируем полученный список как rx)
        response_data = {"rx": ["a", "b", "c"]}

        return web.json_response(response_data)

    except json.JSONDecodeError:
        raise web.HTTPBadRequest(text="Invalid JSON body")