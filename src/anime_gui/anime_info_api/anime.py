import os
from typing import Optional
from anime_gui.anime_info_api.main import _api_request, isAnime_validation, PageParam, isAnime, isAnime_list_validation
from kitsu_extended import Anime


async def get_by_id(anime_id: int) -> Anime:
    result = await _api_request(lambda client: client.get_anime(anime_id))
    assert isAnime_validation(result)
    return result


async def find_by_name(
    anime_name: str,
    page_param: Optional[PageParam] = None,
) -> list[Anime]:
    limit, offset = int(os.getenv("DEFAULT_DEFAULT_PAGE_REQUEST_LIMIT", 20)), 0
    if page_param is not None:
        limit, offset = page_param.limit, page_param.offset

    result = await _api_request(lambda client: client.search_anime(anime_name, limit, offset))

    if isAnime(result):
        result = [result]
    
    assert isAnime_list_validation(result)

    return result
