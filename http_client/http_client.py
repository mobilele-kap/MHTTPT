import asyncio
import aiohttp
import json


class HTTPClient:

    def __init__(self, base_url: str, token: str, interval_check=1):
        self.base_url = base_url
        self.token = token
        self.headers = {
            "token": self.token,
            "Content-Type": "application/json"
        }
        self.interval_check = interval_check
        self.is_connect = None
        self.enabled_loop_check = False

    async def ping(self):
        """/ping"""
        url = f"{self.base_url}/ping"

        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(url, headers=self.headers) as response:
                    if response.status == 204:
                        return True
                    else:
                        text = await response.text()
                        print(f"Response: {text}")
                        print("❌ /ping - FAILED")
                        return False
            except Exception as e:
                print(f"❌ Error: {e}")
                return None

    async def _loop_check(self):
        self.enabled_loop_check = True
        while self.enabled_loop_check:
            result = await self.ping()
            self.is_connect = bool(result)
            await asyncio.sleep(self.interval_check)

    async def create_connection(self, host: str, port: int):
        """Создание подключения через /connect"""
        url = f"{self.base_url}/connect"
        params = {"host": host, "port": port}

        async with aiohttp.ClientSession() as session:
            try:
                async with session.post(url, headers=self.headers, params=params) as response:
                    if response.status == 200:
                        result = await response.json()
                        print(f"Response: {json.dumps(result, indent=2)}")
                        print("✅ /connect - SUCCESS")
                        return result.get("connect_id")
                    else:
                        text = await response.text()
                        print(f"Response: {text}")
                        print("❌ /connect - FAILED")
                        return None
            except Exception as e:
                print(f"❌ Error: {e}")
                return None

    async def delete_connection(self, connect_id: int):
        """Удаление подключения через /disconnect"""
        url = f"{self.base_url}/disconnect"
        params = {"connect_id": connect_id}

        async with aiohttp.ClientSession() as session:
            try:
                async with session.post(url, headers=self.headers, json=params) as response:
                    if response.status == 204:
                        print("✅ /disconnect - SUCCESS")
                        return True
                    else:
                        text = await response.text()
                        print(f"Response: {text}")
                        print("❌ /disconnect - FAILED")
                        return False
            except Exception as e:
                print(f"❌ Error: {e}")
                return False

    async def process_data(self, connect_id: int, tx_list: list):
        """
        Обработка данных через /d

        Args:
            connect_id: ID подключения
            tx_list: список данных для обработки
        """
        url = f"{self.base_url}/d"
        params = {
            'connect_id': connect_id
        }
        body = {"tx": tx_list}

        async with aiohttp.ClientSession() as session:
            try:
                async with session.post(url, headers=self.headers, json=body, params=params) as response:

                    if response.status == 200:
                        result = await response.json()
                        print("✅ /d - SUCCESS")
                        return result
                    else:
                        text = await response.text()
                        print(f"Response: {text}")
                        print("❌ /d - FAILED")
                        return None
            except Exception as e:
                print(f"❌ Error: {e}")
                return None