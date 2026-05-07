from aiohttp import web
from .connect import connect
from .disconnect import disconnect
from .ping import ping
from .data import data
import asyncio

class HTTPServer:

    def __init__(self, host: str, port: int):
        self.host = host
        self.port = port
        self.is_work = False
        self.app = None

    def start_server(self):
        self.app = web.Application()
        self.app.router.add_get("/ping", ping)
        self.app.router.add_post("/connect", connect)
        self.app.router.add_post("/disconnect", disconnect)
        self.app.router.add_post("/d", data)
        asyncio.create_task(self._loop())

    def stop_server(self):
        self.is_work = False

    async def _loop(self):
        runner = web.AppRunner(self.app)
        await runner.setup()
        site = web.TCPSite(runner, self.host, self.port)
        await site.start()
        self.is_work = True
        while self.is_work:
            await asyncio.sleep(1)
        await site.stop()


