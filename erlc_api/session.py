import aiohttp
import asyncio
from typing import Optional


class SVSessionManager:
    """
    Manages aiohttp sessions for SVAPIHELPER:LC
    - Shared session
    - Auto reopen
    - Auto close
    - Session pooling
    """

    def __init__(self):
        self.session: Optional[aiohttp.ClientSession] = None
        self._lock = asyncio.Lock()

    async def get_session(self) -> aiohttp.ClientSession:
        async with self._lock:
            if self.session is None or self.session.closed:
                self.session = aiohttp.ClientSession()
            return self.session

    async def close(self):
        if self.session and not self.session.closed:
            await self.session.close()


class SVAPISession:
    """
    Clean context manager for calling the ERLC API:

    async with sv.session() as api:
        await api.get_server_info()
    """

    def __init__(self, api):
        self.api = api

    async def __aenter__(self):
        return self.api

    async def __aexit__(self, exc_type, exc, tb):
        return False
