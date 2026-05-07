import asyncio
import socket
from typing import Optional, Callable
from . import exceptions


class SocketServer:
    def __init__(self, host: str = 'localhost', port: int = 10000, n_bytes: int = 1024, callback: Callable = None):
        self.host = host
        self.port = port
        self.socket = None
        self.n_bytes = n_bytes
        self.is_work = False
        self.callback = callback
        self.handle_delay = 0.001
        self.clients = {}
        self.loop = asyncio.get_event_loop()

    async def handle_client_async(self, client_socket: socket.socket, client_addr: tuple):
        """Асинхронная обработка клиента с низкоуровневым socket"""
        print(f"Новое подключение от {client_addr}")

        try:
            while True:
                # Асинхронное чтение данных
                data = await self.loop.sock_recv(client_socket, self.n_bytes)

                if not data:
                    self.disconnect_client_handle(client_addr)
                    break

                print(f"Получено от {client_addr}: {len(data)}B")
                self.callback and self.callback({'event': 'data', 'client_addr': client_addr, 'data': data})
                await asyncio.sleep(self.handle_delay)

        except Exception as e:
            print(f"Ошибка при обработке {client_addr}: {e}")
        finally:
            client_socket.close()

    def disconnect_client_handle(self, client_addr: tuple):
        """Обработка закрытия"""
        client = self.clients.get(client_addr)
        if not client:
            raise exceptions.ClientNotFound(client_addr)
        print(f"Клиент {client_addr} отключился")
        del self.clients[client_addr]
        self.callback and self.callback({'event': 'disconnect', 'client_addr': client_addr})

    async def send_client(self, client_addr: tuple, data: bytes):
        client = self.clients.get(client_addr)
        if not client:
            raise exceptions.ClientNotFound(client_addr)
        client_socket = client.get('socket')
        await self.loop.sock_sendall(client_socket, data)

    async def _receiver_connections(self):
        """Цикл для принятия соединений"""
        try:
            while True:
                client_socket, client_addr = await self.loop.sock_accept(self.socket)
                self.clients[client_addr] = {"socket": client_socket}
                # Запускаем обработку клиента в отдельной корутине
                asyncio.create_task(self.handle_client_async(client_socket, client_addr))
                self.callback and self.callback({'event': 'connect', 'client_addr': client_addr})
        except KeyboardInterrupt:
            print("\nОстановка сервера...")
        finally:
            self.socket.close()

    async def _loop(self):
        task_receiver = asyncio.create_task(self._receiver_connections())
        while self.is_work:
            await asyncio.sleep(1)
        task_receiver.cancel()

    def start(self):
        """Запуск низкоуровневого сервера"""
        self.is_work = True
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind((self.host, self.port))
        self.socket.listen(10)
        self.socket.setblocking(False)
        asyncio.create_task(self._loop())

if __name__ == '__main__':
    async def main():
        server = SocketServer()
        server.start()

    asyncio.run(main())