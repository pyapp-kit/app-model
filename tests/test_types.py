import pytest
from pydantic import ValidationError

from app_model.types import Action, Icon


def test_icon_validate():
    assert Icon._validate('"fa6s.arrow_down"') == Icon(
        dark='"fa6s.arrow_down"', light='"fa6s.arrow_down"'
    )


def test_action_validation():
    with pytest.raises(ValidationError, match="'s!adf' is not a valid python_name"):
        Action(id="test", title="test", callback="s!adf")

    with pytest.raises(ValidationError):
        Action(id="test", title="test", callback=[])

    with pytest.raises(ValidationError, match="'x.<locals>:asdf' is not a valid"):
        Action(id="test", title="test", callback="x.<locals>:asdf")
