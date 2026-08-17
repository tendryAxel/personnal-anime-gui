from anime_gui.anime_info_api import anime


def test_get_anime_by_id():
    anime_id = 21
    result = anime.get_by_id(anime_id)

    assert result.id == str(anime_id)
    assert result.title == "Neon Genesis Evangelion"

def test_find_anime_by_name():
    result = anime.find_by_name("recoil")

    assert isinstance(result, list)
    assert len(result) >= 3
    assert result[0].title == "Lycoris Recoil"
