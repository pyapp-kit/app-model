import sys
from typing import ClassVar

import pytest
from pydantic_compat import PYDANTIC2, BaseModel

from app_model.types import (
    KeyBinding,
    KeyBindingRule,
    KeyCode,
    KeyMod,
    SimpleKeyBinding,
)
from app_model.types._keys import KeyChord, KeyCombo, StandardKeyBinding

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
    assert kb == SimpleKeyBinding._parse_input(f"{_mod}{key}")
    # or with a string
    assert kb == f"{_mod}{key}"
    assert kb != ["A", "B"]  # check type error during comparison

    # round trip to int
    assert isinstance(kb.to_int(), KeyCombo)
    # using validate method just for test coverage... will pass to from_int
    assert SimpleKeyBinding._parse_input(int(kb)) == kb
    assert SimpleKeyBinding._parse_input(kb) == kb

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


def test_chord_keybinding() -> None:
    kb = KeyBinding.from_str("Shift+A Cmd+9")
    assert len(kb) == 2
    assert kb != "Shift+A Cmd+9"  # comparison with string considered anti-pattern
    assert kb == KeyBinding.from_str("Shift+A Cmd+9")
    assert kb.part0 == SimpleKeyBinding(shift=True, key=KeyCode.KeyA)
    assert kb.part0 == "Shift+A"
    assert str(kb) in repr(kb)
    # round trip to int
    assert isinstance(kb.to_int(), KeyChord)
    # using validate method just for test coverage... will pass to from_int
    assert KeyBinding.validate(int(kb)) == kb
    assert KeyBinding.validate(kb) == kb


def test_in_dict():
    a = SimpleKeyBinding.from_str("Shift+A")
    b = KeyBinding.from_str("Shift+B")

    try:
        kbs = {
            a: 0,
            b: 1,
        }
    except TypeError as e:
        if str(e).startswith("unhashable type"):
            pytest.fail(f"keybinds not hashable: {e}")
        else:
            raise e

    assert kbs[a] == 0
    assert kbs[b] == 1

    new_a = KeyBinding.from_str("Shift+A")

    with pytest.raises(KeyError):
        kbs[new_a]


def test_in_model():
    class M(BaseModel):
        key: KeyBinding

        if not PYDANTIC2:

            class Config:
                json_encoders: ClassVar[dict] = {KeyBinding: str}

    m = M(key="Shift+A B")
    # pydantic v1 and v2 have slightly different json outputs
    assert m.model_dump_json().replace('": "', '":"') == '{"key":"Shift+A B"}'


def test_standard_keybindings():
    class M(BaseModel):
        key: KeyBindingRule

    m = M(key=StandardKeyBinding.Copy)
    assert m.key.primary == KeyMod.CtrlCmd | KeyCode.KeyC
