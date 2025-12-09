import time
import asyncio
from .errors import *


class CacheManager:
    def __init__(self):
        self._cache = {}

    def get(self, key):
        entry = self._cache.get(key)
        if not entry:
            return None
        expire, value = entry
        if time.time() > expire:
            self._cache.pop(key, None)
            return None
        return value

    def set(self, key, value, ttl):
        self._cache[key] = (time.time() + ttl, value)


cache = CacheManager()


async def retry_api_call(func, retries=3):
    for attempt in range(retries):
        try:
            return await func()
        except RateLimitError:
            await asyncio.sleep(1)
        except Exception:
            if attempt == retries - 1:
                raise
            await asyncio.sleep(0.5)


def check_response(status: int, data: dict):
    if status == 401:
        raise AuthenticationError(data.get("message"))
    if status == 404:
        raise NotFoundError(data.get("message"))
    if status == 429:
        raise RateLimitError("ERLC API Rate Limit hit.")
    if status >= 400:
        raise UnknownAPIError(f"{status}: {data}")
