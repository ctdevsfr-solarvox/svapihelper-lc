import aiohttp
from .errors import *
from .models import *
from .session import *
from .utils import cache, retry_api_call, check_response


class SVAPI:
    BASE_URL = "https://api.policeroleplay.community/v1/"

    def __init__(self, api_key: str, session_manager: SVSessionManager = None):
        self.api_key = api_key
        self.manager = session_manager or SVSessionManager()

    # ---------------------------
    # Session Context
    # ---------------------------
    def session(self):
        return SVAPISession(self)

    # ---------------------------
    # Internal request method
    # ---------------------------
    async def _request(self, method: str, endpoint: str, *, payload=None):
        session = await self.manager.get_session()

        async def call():
            async with session.request(
                method,
                self.BASE_URL + endpoint,
                headers={"Authorization": self.api_key},
                json=payload
            ) as r:
                data = await r.json()
                check_response(r.status, data)
                return data

        return await retry_api_call(call)

    # ---------------------------
    # GET + Caching support
    # ---------------------------
    async def _get(self, endpoint: str, *, cache_ttl: int = 0):
        cache_key = f"GET:{endpoint}"
        if cache_ttl:
            cached_data = cache.get(cache_key)
            if cached_data:
                return cached_data

        data = await self._request("GET", endpoint)
        if cache_ttl:
            cache.set(cache_key, data, cache_ttl)

        return data

    # ---------------------------
    # POST
    # ---------------------------
    async def _post(self, endpoint: str, payload: dict):
        return await self._request("POST", endpoint, payload=payload)

    # ======================================================
    #                      API ENDPOINTS
    # ======================================================

    async def get_server_info(self, cache=3):
        """Returns server data with optional caching"""
        data = await self._get("server", cache_ttl=cache)
        return ServerInfo.from_dict(data)

    async def get_player(self, user_id: int, cache=2):
        """Returns player info"""
        data = await self._get(f"players/{user_id}", cache_ttl=cache)
        return Player.from_dict(data)

    async def get_calls(self, cache=2):
        """Returns list of active calls"""
        data = await self._get("calls", cache_ttl=cache)
        return [Call.from_dict(c) for c in data]

    async def send_event(self, event_type: str, department: str):
        """Send a custom ERLC event"""
        return await self._post("events", {"event": event_type, "department": department})
