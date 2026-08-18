import os
from typing import Optional
from anime_gui.anime_info_api.main import _api_request, isAnime_validation, PageParam, isAnime, isAnime_list_validation, CachingUtilities
from kitsu_extended import Anime


@CachingUtilities.async_caching
async def get_by_id(anime_id: int) -> Anime:
    request_key = CachingUtilities._make_cache_key("get_by_id", {"id": anime_id})
    
    result = await _api_request(lambda client: client.get_anime(anime_id), key=request_key)
    assert isAnime_validation(result)
    return result


@CachingUtilities.async_caching
async def find_by_name(
    anime_name: str,
    page_param: Optional[PageParam] = None,
) -> list[Anime]:
    limit, offset = int(os.getenv("DEFAULT_DEFAULT_PAGE_REQUEST_LIMIT", 20)), 0
    if page_param is not None:
        limit, offset = page_param.limit, page_param.offset

    request_key = CachingUtilities._make_cache_key("find_by_name", {"name": anime_name, "page": page_param})

    result = await _api_request(lambda client: client.search_anime(anime_name, limit, offset), key=request_key)

    if isAnime(result):
        result = [result]
    
    assert isAnime_list_validation(result)

    return result
