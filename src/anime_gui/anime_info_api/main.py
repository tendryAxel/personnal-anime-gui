from typing import TypeIs
import asyncio
import kitsu_extended as kitsu


def isAnime_validation(to_valid) -> TypeIs[kitsu.Anime]:
    if isinstance(to_valid, kitsu.Anime):
        return True
    
    raise TypeError(f"Need parsing implementation of {type(to_valid) = }, that contains: {to_valid}")

def get_by_id(anime_id: int) -> kitsu.Anime:
    async def async_get_by_id(anime_id: int) -> kitsu.Anime | dict:
        client = kitsu.Client()

        try:
            return await client.get_anime(anime_id)
        finally:
            await client.close()
            
    result = asyncio.run(async_get_by_id(anime_id))

    assert isAnime_validation(result)

    return result
