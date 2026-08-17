from anime_gui.anime_info_api.main import _api_request, isAnime_validation
import asyncio
import kitsu_extended as kitsu


def get_by_id(anime_id: int) -> kitsu.Anime:
    result = asyncio.run(_api_request(lambda client: client.get_anime(anime_id)))

    assert isAnime_validation(result)

    return result
