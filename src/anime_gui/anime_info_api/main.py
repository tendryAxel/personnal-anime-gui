from anime_gui.settings import home_setting_path
import inspect
import datetime
from diskcache import Cache
from collections.abc import Callable, Coroutine, Awaitable
from functools import wraps
from ast import arg
import base64
import pickle
import dataclasses
from types import CoroutineType
from typing import TypeIs, Any
import kitsu_extended as kitsu
import dotenv
import hashlib
import json
import time

dotenv.load_dotenv()


class CachingUtilities:
    cache = Cache(home_setting_path / "cache")
    byte_encoding = "ascii"

    @staticmethod
    def _make_cache_key(function_hashed: str, args: dict[str, Any]):
        payload = {
            "url": function_hashed,
            "params": args,
        }

        raw = json.dumps(
            payload,
            sort_keys=True,
            default=str,
        )

        print(f"Raw: {raw}")

        return hashlib.sha256(raw.encode()).hexdigest()
    
    @staticmethod
    def serialize[T](obj: T) -> str:
        pickled = pickle.dumps(obj)
        return base64.b64encode(pickled).decode(CachingUtilities.byte_encoding)

    @staticmethod
    def deserialize[T](value: str) -> T:
        pickled = base64.b64decode(value.encode(CachingUtilities.byte_encoding))
        return pickle.loads(pickled)
    
    @classmethod
    def async_caching[**P, T](cls, func: Callable[P, Awaitable[T]]) -> Callable[P, Awaitable[T]]:
        @wraps(func)
        async def inner(*args: P.args, **kwargs: P.kwargs) -> T:
            func_source = inspect.getsource(func)
            func_hash = hashlib.sha256(func_source.encode("utf-8")).hexdigest()
            
            request_key = cls._make_cache_key(
                func_hash,
                {
                    **{str(i): value for i, value in enumerate(args)},
                    **kwargs,
                }
            )

            cached = cls.cache.get(request_key)
            if cached is not None:
                print(f"Cache HIT for the {request_key = }")
                return cls.deserialize(cached)

            result = await func(*args, **kwargs)
            print(f"Cache MISS for the {request_key = }")

            cls.cache.add(
                request_key, cls.serialize(result),
                expire=datetime.timedelta(days=3).total_seconds()
            )

            return result

        return inner
    
    @classmethod
    def caching[**P, T](cls, func: Callable[P, T]) -> Callable[P, T]:
        @wraps(func)
        def inner(*args: P.args, **kwargs: P.kwargs) -> T:
            func_source = inspect.getsource(func)
            func_hash = hashlib.sha256(func_source.encode("utf-8")).hexdigest()
            
            request_key = cls._make_cache_key(
                func_hash,
                {
                    **{str(i): value for i, value in enumerate(args)},
                    **kwargs,
                }
            )

            cached = cls.cache.get(request_key)
            if cached is not None:
                print(f"Cache HIT for the {request_key = }")
                return cls.deserialize(cached)

            result = func(*args, **kwargs)
            print(f"Cache MISS for the {request_key = }")

            cls.cache.add(
                request_key, cls.serialize(result),
                expire=datetime.timedelta(days=3).total_seconds()
            )

            return result

        return inner

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
    client = kitsu.Client()

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
