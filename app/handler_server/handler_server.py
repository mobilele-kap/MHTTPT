from app.socket_server import SocketServer
from typing import Callable
from app.utils.limited_queue import LimitedQueue


class HandlerServer:

    def __init__(self, host: str, port: int, n_bytes: int = 1024, limit_queue = 1000):
        self.server = SocketServer(host=host, port=port, n_bytes=n_bytes, callback=self.call_back_handler)

    def start(self):
        self.server.start()

    def call_back_handler(self, event):
        pass