import asyncio
import json
from app.utils.logger import logger
from random import randint
from . import exceptions
from typing import Optional, Callable


class SocketClient:
    def __init__(self, host: str, port: int, n_bytes: int = 1024, limit_connections = 128, callback: Callable=None, handle_delay=0.001):
        self.host = host
        self.port = port
        self.n_bytes = n_bytes
        self.limit_connections = limit_connections
        self.callback = callback
        self.handle_delay = handle_delay
        self.connections = {}

    def get_free_id(self):
        while True:
            new_id = randint(0,2_147_483_647)
            if new_id not in self.connections:
                return new_id

    async def connect(self):
        """Установка соединения"""
        try:
            if len(self.connections) >= self.limit_connections:
                raise exceptions.ConnectionsOverflow
            reader, writer = await asyncio.open_connection(
                self.host,
                self.port
            )
            connect_id = self.get_free_id()
            self.connections[connect_id] = {'reader': reader, 'writer': writer}
            logger.info(f"Подключен к {self.host}:{self.port}")
            return connect_id
        except Exception as e:
            logger.error(f"Ошибка подключения: {e}")
            raise e

    async def handle_client_async(self, reader: asyncio.StreamReader, connect_id: int):
        try:
            while True:
                data = await reader.read(self.n_bytes)
                if not data:
                    self.disconnect_client_handle(connect_id)
                    break
                print(f"Получено от {connect_id}: {len(data)}B")
                self.callback and self.callback({'event': 'data', 'connect_id': connect_id, 'data': data})
                await asyncio.sleep(self.handle_delay)
        except Exception as e:
            logger.error(f"Ошибка получения: {e}")
            raise

    def disconnect_client_handle(self, connect_id: int):
        """Обработка закрытия"""
        client = self.connections.get(connect_id)
        if not client:
            raise exceptions.ConnectionsNotFound(connect_id)
        print(f"Сервер {connect_id} отключился")
        del self.connections[connect_id]
        self.callback and self.callback({'event': 'disconnect', 'connect_id': connect_id})

    async def send_server(self, connect_id: int, data: bytes):
        """Отправка сообщения"""
        connect = self.connections.get(connect_id)
        if not connect:
            raise exceptions.ConnectionsNotFound(connect_id)
        writer = connect.get('writer')
        writer.write(data)
        await writer.drain()
        logger.debug(f"Отправлено: {connect_id} {len(data)}")

    async def close(self, connect_id: int):
        """Закрытие соединения"""
        connect = self.connections.get(connect_id)
        if not connect:
            raise exceptions.ConnectionsNotFound(connect_id)
        writer = connect.get('writer')
        writer.close()
        del self.connections[connect_id]
        await writer.wait_closed()
        logger.info(f"Соединение {connect_id} закрыто")
