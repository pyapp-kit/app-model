import sys

import pytest

from app_model.types import KeyBinding, KeyCode, KeyMod, SimpleKeyBinding
from app_model.types._keys import KeyChord, KeyCombo

MAC = sys.platform == "darwin"


@pytest.mark.parametrize("key", list("ADgf`]/,"))
@pytest.mark.parametrize("mod", ["ctrl", "shift", "alt", "meta", None])
def test_simple_keybinding_single_mod(mod: str, key: str) -> None:
    _mod = f"{mod}+" if mod else ""
    kb = SimpleKeyBinding.from_str(f"{_mod}{key}")
    assert str(kb).lower() == f"{_mod}{key}".lower()
    assert not kb.is_modifier_key()

    # we can compare it with another SimpleKeyBinding
    # using validate method just for test coverage... will pass to from_str
    assert kb == SimpleKeyBinding.validate(f"{_mod}{key}")
    # or with a string
    assert kb == f"{_mod}{key}"
    assert kb != ["A", "B"]  # check type error during comparison

    # round trip to int
    assert isinstance(kb.to_int(), KeyCombo)
    # using validate method just for test coverage... will pass to from_int
    assert SimpleKeyBinding.validate(int(kb)) == kb
    assert SimpleKeyBinding.validate(kb) == kb

    # first part of a Keybinding is a simple keybinding
    as_full_kb = KeyBinding.validate(kb)
    assert as_full_kb.part0 == kb
    assert KeyBinding.validate(int(kb)).part0 == kb

    assert int(as_full_kb) == int(kb)


def test_simple_keybinding_multi_mod():
    # here we're also testing that cmd and win get cast to 'KeyMod.CtrlCmd'

    kb = SimpleKeyBinding.from_str("cmd+shift+A")
    assert not kb.is_modifier_key()
    assert int(kb) & KeyMod.CtrlCmd | KeyMod.Shift

    kb = SimpleKeyBinding.from_str("win+shift+A")
    assert not kb.is_modifier_key()
    assert int(kb) & KeyMod.CtrlCmd | KeyMod.Shift

    kb = SimpleKeyBinding.from_str("win")  # just a modifier
    assert kb.is_modifier_key()


def test_chord_keybinding():
    kb = KeyBinding.from_str("Shift+A Cmd+9")
    assert len(kb) == 2
    assert kb == "Shift+A Cmd+9"
    assert kb == KeyBinding.from_str("Shift+A Cmd+9")
    assert kb.part0 == SimpleKeyBinding(shift=True, key=KeyCode.KeyA)
    assert kb.part0 == "Shift+A"

    # round trip to int
    assert isinstance(kb.to_int(), KeyChord)
    # using validate method just for test coverage... will pass to from_int
    assert KeyBinding.validate(int(kb)) == kb
    assert KeyBinding.validate(kb) == kb


def test_in_model():
    from pydantic import BaseModel

    class M(BaseModel):
        key: KeyBinding

        class Config:
            json_encoders = {KeyBinding: str}

    m = M(key="Shift+A B")
    assert m.json(models_as_dict=False) == '{"key": "Shift+A B"}'
