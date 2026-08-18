import dataclasses
from types import CoroutineType
from typing import TypeIs, Callable, Any
import kitsu_extended as kitsu
import dotenv

dotenv.load_dotenv()


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
