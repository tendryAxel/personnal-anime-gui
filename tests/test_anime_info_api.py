from anime_gui.anime_info_api import anime


def test_get_by_id():
    anime_id = 21
    result = anime.get_by_id(anime_id)

    assert result.id == str(anime_id)
    assert result.title == "Neon Genesis Evangelion"
