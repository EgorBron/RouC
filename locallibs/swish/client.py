import aiohttp
import asyncio
import typing
from listener import Listener
def _raise_everywhere(exc: Exception):
    raise exc
def listener(func):
    def wrapper(eventname:str='noevent', **kwargs):
        return Listener(func.__qualname__ or eventname, func)
    return wrapper

class Client:
    def __init__(self, bot):
        self.listeners = []
    def add_listener(self, func: Listener):
        self.listeners.append(func)
    async def prepare_swish(self):
        if not self.first_ready:
            return
        self._swish_session = aiohttp.ClientSession()
        self._swish_websocket = await self._swish_session.ws_connect(
            url=f'ws://127.0.0.1:8000',
            headers={
                'Authorization': "roucswish",
                'User-Agent':    'Python/v3.9.6,swish.py/v0.0.1a',
                'User-Id':       str(self.user.id),
            },
        )
        self.swish_task = asyncio.create_task(self._listen())

    async def _listen(self) -> None:
        while True:
            message = await self._swish_websocket.receive()
            payload = message.json()

            asyncio.create_task(self._receive_payload(payload['op'], data=payload['d']))

    async def _receive_payload(self, op: str, /, *, data: dict[str, typing.Any]) -> None:
        raise NotImplementedError

    async def _send_payload(self, op: str, data: dict[str, typing.Any]) -> None:

        await self._swish_websocket.send_json(
            data={
                'op': op,
                'd':  data,
            }
        )