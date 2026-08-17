from types import CoroutineType
from typing import TypeIs, Callable, Any
import asyncio
import kitsu_extended as kitsu


def isAnime_validation(to_valid) -> TypeIs[kitsu.Anime]:
    if isinstance(to_valid, kitsu.Anime):
        return True
    
    raise TypeError(f"Need parsing implementation of {type(to_valid) = }, that contains: {to_valid}")

async def _api_request[T](request: Callable[[kitsu.Client], CoroutineType[Any, Any, T]]) -> T:
    client = kitsu.Client()

    try:
        return await request(client)
    finally:
        await client.close()

def get_by_id(anime_id: int) -> kitsu.Anime:
    result = asyncio.run(_api_request(lambda client: client.get_anime(anime_id)))

    assert isAnime_validation(result)

    return result
