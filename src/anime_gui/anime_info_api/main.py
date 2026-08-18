import base64
import pickle
import dataclasses
from types import CoroutineType
from typing import TypeIs, Callable, Any
import kitsu_extended as kitsu
import dotenv
import hashlib
import json
import time

dotenv.load_dotenv()


# TODO: create a decoration instead
class CachingUtilities:
    cache: dict[str, str] = {}
    byte_encoding = "ascii"

    @staticmethod
    def _make_cache_key(function_name: str, args: dict[str, Any]):
        payload = {
            "url": function_name,
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

async def _api_request[T](request: Callable[[kitsu.Client], CoroutineType[Any, Any, T]], key: str) -> T:
    cache_content = CachingUtilities.cache.get(key)

    if cache_content is not None:
        print(f"Cache HIT for the {key = }")
        return CachingUtilities.deserialize(cache_content)

    client = kitsu.Client()

    try:
        print(f"Cache MISS for the {key = }")
        result = await request(client)
        CachingUtilities.cache[key] = CachingUtilities.serialize(result)
        return result
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
