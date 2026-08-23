import os

from kitsu_extended import Anime

from anime_info_api.main import (
    CachingUtilities,
    PageParam,
    _api_request,
    isAnime,
    isAnime_list_validation,
    isAnime_validation,
)


@CachingUtilities.async_caching
async def get_by_id(anime_id: int) -> Anime:
    result = await _api_request(lambda client: client.get_anime(anime_id))
    assert isAnime_validation(result)
    return result


@CachingUtilities.async_caching
async def find_by_name(
    anime_name: str,
    page_param: PageParam | None = None,
) -> list[Anime]:
    limit, offset = int(os.getenv("DEFAULT_DEFAULT_PAGE_REQUEST_LIMIT", 20)), 0
    if page_param is not None:
        limit, offset = page_param.limit, page_param.offset

    result = await _api_request(
        lambda client: client.search_anime(anime_name, limit, offset)
    )

    if isAnime(result):
        result = [result]

    assert isAnime_list_validation(result)

    return result
