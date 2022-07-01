from app_model.types import Icon


def test_icon_validate():
    assert Icon.validate('"fa5s.arrow_down"') == Icon(
        dark='"fa5s.arrow_down"', light='"fa5s.arrow_down"'
    )
