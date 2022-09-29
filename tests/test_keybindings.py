import sys
from typing import Dict, List

import pytest
from pydantic import BaseModel, ValidationError

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


def test_custom_root_type():
    kb = KeyBinding.from_str("shift+a cmd+9")

    assert str(kb) == "Shift+A Meta+9"
    assert kb.parts == [
        SimpleKeyBinding.from_str("Shift+A"),
        SimpleKeyBinding.from_str("Cmd+9"),
    ]

    kb.__root__ = "Ctrl+C Ctrl+V"
    assert kb.parts == [
        SimpleKeyBinding.from_str("Ctrl+C"),
        SimpleKeyBinding.from_str("Ctrl+V"),
    ]


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
            pytest.fail("keybinds not hashable")
        else:
            raise e

    assert kbs[hash(a)] == 0
    assert kbs[hash(b)] == 1

    new_a = KeyBinding.from_int(hash(a))

    with pytest.raises(KeyError):
        kbs[new_a]

    assert kbs[hash(new_a)] == 0


def test_errors():
    with pytest.raises(ValidationError, match="field required"):
        KeyBinding()

    with pytest.raises(ValidationError, match="not a valid list"):
        KeyBinding(parts=None)

    with pytest.raises(ValidationError, match="not a valid list"):
        KeyBinding(parts=tuple())

    with pytest.raises(ValidationError, match="at least 1 items"):
        KeyBinding(parts=[])

    with pytest.raises(ValidationError, match="at least 1 items"):
        KeyBinding(__root__="")

    kb = KeyBinding.parse_obj("Cmd+R")

    with pytest.raises(ValidationError, match="not a valid list"):
        kb.parts = None

    with pytest.raises(ValidationError, match="not a valid list"):
        kb.parts = set()

    with pytest.raises(ValidationError, match="at least 1 items"):
        kb.parts = []

    with pytest.raises(ValidationError, match="at least 1 items"):
        kb.__root__ = ""


def test_in_model():
    class M(BaseModel):
        key: KeyBinding

        class Config:
            json_encoders = {KeyBinding: str}

    m = M(key="Shift+A B")
    assert m.json() == '{"key": "Shift+A B"}'


def test_in_nested_model():
    class M(BaseModel):
        keybinds: Dict[str, List[KeyBinding]]

    class N(BaseModel):
        m: M

    n = N(m=M(keybinds={"abc": ["Shift+A B", "Shift+C D"]}))
    assert n.json() == '{"m": {"keybinds": {"abc": ["Shift+A B", "Shift+C D"]}}}'


def test_standard_keybindings():
    class M(BaseModel):
        key: KeyBindingRule

    m = M(key=StandardKeyBinding.Copy)
    assert m.key.primary == KeyMod.CtrlCmd | KeyCode.KeyC
