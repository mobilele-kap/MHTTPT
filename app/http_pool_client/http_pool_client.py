from typing import List, Dict
from app.http_client import HTTPClient
from app.utils.limited_queue import LimitedQueue
import asyncio


class HttpPoolClient:

    def __init__(self, hosts: List[str], token: str, interval_check: int = 1):
        """
        :param hosts: ['http://127.0.0.1:8080']
        """
        self.hosts = hosts
        self.token = token
        self.interval_check = interval_check
        self.clients = {}
        self.tx_queue = LimitedQueue(10000)
        self.rx_queue = LimitedQueue(10000)
        self.is_work_send_handler = False

    def start(self):
        for host in self.hosts:
            if host not in self.clients:
                client = HTTPClient(host=host, token=self.token, interval_check=self.interval_check)
                self.clients[host] = client
                client.start()
        self.is_work_send_handler = True
        asyncio.create_task(self._send_handler)

    async def send_data(self, connect_id: int, tx_list: list):
        for data_part in [tx_list[i:i + 8] for i in range(0, len(tx_list), 8)]:
            self.tx_queue.put((connect_id, data_part))

    async def _get_data(self, client, connect_id, tx_list):
        pass

    async def _send_handler(self):
        while self.is_work_send_handler:
            for host, client in self.clients.items():
                if not client.is_connect:
                    continue
                item = self.tx_queue.get()
                if item is None:
                    pass



