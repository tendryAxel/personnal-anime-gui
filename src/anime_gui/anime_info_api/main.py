import asyncio
import kitsu_extended as kitsu


async def async_get_by_id(anime_id: int) -> kitsu.Anime | dict:
    client = kitsu.Client()

    try:
        return await client.get_anime(anime_id)
    finally:
        await client.close()


def get_by_id(anime_id: int) -> kitsu.Anime:
    result = asyncio.run(async_get_by_id(anime_id))

    if isinstance(result, kitsu.Anime):
        return result
    
    raise Exception(f"Need parsing implementation of {type(result) = }, that contains\n{result}")