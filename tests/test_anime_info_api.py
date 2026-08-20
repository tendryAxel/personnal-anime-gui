import pytest
from anime_info_api import anime


@pytest.mark.asyncio
async def test_get_anime_by_id():
    anime_id = 21
    result = await anime.get_by_id(anime_id)

    assert result.id == str(anime_id)
    assert result.title == "Neon Genesis Evangelion"

@pytest.mark.asyncio
async def test_find_anime_by_name():
    result = await anime.find_by_name("recoil")

    assert isinstance(result, list)
    assert len(result) >= 3
    assert result[0].title == "Lycoris Recoil"
