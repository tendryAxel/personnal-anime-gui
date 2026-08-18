import dataclasses
from types import CoroutineType
from typing import TypeIs, Callable, Any
import kitsu_extended as kitsu
import dotenv
import hashlib
import json
import time

dotenv.load_dotenv()


class CachedClient(kitsu.Client):
    def __init__(self, *args, cache_ttl=3600, **kwargs):
        super().__init__(*args, **kwargs)

        self.cache_ttl = cache_ttl
        self.cache = {}
    
    def serialize(self, obj):
        if isinstance(obj, dict):
            return "{" + ",".join(
                f"{self.serialize(k)}:{self.serialize(v)}"
                for k, v in sorted(obj.items(), key=lambda x: str(x[0]))
            ) + "}"
        if isinstance(obj, (list, tuple)):
            return "[" + ",".join(self.serialize(x) for x in obj) + "]"
        return repr(obj)

    def _make_cache_key(self, url, kwargs):
        payload = {
            "url": url,
            "params": kwargs.get("params", {}),
        }

        raw = json.dumps(
            payload,
            sort_keys=True,
            default=str,
        )

        print(f"Raw: {raw}")

        return hashlib.sha256(raw.encode()).hexdigest()

    async def _get(self, url: str, **kwargs):
        key = self._make_cache_key(url, kwargs)

        cached = self.cache.get(key)

        if cached is not None:
            timestamp, data = cached

            if time.time() - timestamp < self.cache_ttl:
                print("CACHE HIT:", url)
                return data

            del self.cache[key]

        # Not cached -> let the original library make the request
        print("CACHE MISS:", url, kwargs)
        print(f"cache content: {self.cache}")

        data = await super()._get(url, **kwargs)

        self.cache[key] = (time.time(), data)

        return data

def isAnime(to_valid) -> TypeIs[kitsu.Anime]:
    if isinstance(to_valid, kitsu.Anime):
        return True
    
    return False


def isAnime_validation(to_valid) -> TypeIs[kitsu.Anime]:
    if isAnime(to_valid):
        return True
    
    raise TypeError(f"Need parsing implementation of {type(to_valid) = }, that contains: {to_valid}")


def isAnime_list_validation(to_valid) -> TypeIs[list[kitsu.Anime]]:
    for element in to_valid:
        isAnime_validation(element)
    
    return True

async def _api_request[T](request: Callable[[kitsu.Client], CoroutineType[Any, Any, T]]) -> T:
    client = CachedClient()
    
    try:
        return await request(client)
    finally:
        await client.close()

@dataclasses.dataclass
class PageParam:
    page_number: int
    page_size: int

    def __post_init__(self):
        if self.page_number < 0:
            raise ValueError(f"Page number must be positive number, not {self.page_number}")
        
        if self.page_size < 0:
            raise ValueError(f"Page size must be positive number, not {self.page_size}")
    
    @property
    def limit(self):
        return self.page_size
    
    @property
    def offset(self):
        return self.page_size * self.page_number
    
    def next_page(self):
        self.page_number += 1
    
    def previous_page(self):
        self.page_number -= 1
