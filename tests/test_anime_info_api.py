from anime_gui.anime_info_api.main import get_by_id


def test_get_by_id():
    anime_id = 21
    result = get_by_id(anime_id)

    assert result.id == str(anime_id)
    assert result.title == "Neon Genesis Evangelion"
