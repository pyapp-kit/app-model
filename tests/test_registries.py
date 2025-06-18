# mypy: disable-error-code="var-annotated"
import pytest

from app_model.registries import KeyBindingsRegistry, MenusRegistry
from app_model.registries._keybindings_reg import _RegisteredKeyBinding
from app_model.types import (
    Action,
    KeyBinding,
    KeyBindingRule,
    KeyBindingSource,
    KeyCode,
    KeyMod,
    MenuItem,
)


def _noop() -> None:
    pass


def test_menus_registry() -> None:
    reg = MenusRegistry()
    reg.append_menu_items([("file", {"command": {"id": "file.new", "title": "File"}})])
    reg.append_menu_items([("file.sub", {"submenu": "Sub", "title": "SubTitle"})])

    assert isinstance(reg.get_menu("file")[0], MenuItem)
    assert "(2 menus)" in repr(reg)
    assert "File" in str(reg)
    assert "Sub" in str(reg)  # ok to change


def test_keybindings_registry() -> None:
    reg = KeyBindingsRegistry()
    assert "(0 bindings)" in repr(reg)


def test_register_keybinding_rule_filter_type() -> None:
    """Check `_filter_keybinding` type checking when setting."""
    reg = KeyBindingsRegistry()
    with pytest.raises(TypeError, match="'filter_keybinding' must be a callable"):
        reg.filter_keybinding = "string"  # type: ignore


def _filter_fun(kb: KeyBinding) -> str:
    if kb.part0.is_modifier_key():
        return "modifier only sequences not allowed"
    return ""


def test_register_keybinding_rule_filter_get() -> None:
    """Check `_filter_keybinding` getter."""
    reg = KeyBindingsRegistry()
    reg.filter_keybinding = _filter_fun
    assert callable(reg.filter_keybinding)


def test_register_keybinding_rule_filter() -> None:
    """Check `filter_keybinding` in `register_keybinding_rule`."""
    reg = KeyBindingsRegistry()
    reg.filter_keybinding = _filter_fun

    # Valid keybinding
    kb = KeyBindingRule(primary=KeyMod.CtrlCmd | KeyCode.KeyO)
    reg.register_keybinding_rule("test", kb)
    # Invalid keybinding
    kb = KeyBindingRule(primary=KeyMod.Alt)
    with pytest.raises(ValueError, match=r"Alt\+: modifier only"):
        reg.register_keybinding_rule("test", kb)


@pytest.mark.parametrize(
    "kb, msg",
    [
        (
            [
                {"primary": KeyMod.CtrlCmd | KeyCode.KeyA},
                {"primary": KeyMod.Shift | KeyCode.KeyC},
            ],
            "",
        ),
        (
            [{"primary": KeyMod.Alt}, {"primary": KeyMod.Shift}],
            r"Alt\+: modifier only sequences not allowed\nShift\+: modifier",
        ),
    ],
)
def test_register_action_keybindings_filter(kb: list[dict], msg: str) -> None:
    """Check `filter_keybinding` in `register_action_keybindings`."""
    reg = KeyBindingsRegistry()
    reg.filter_keybinding = _filter_fun

    action = Action(
        id="cmd_id1",
        title="title1",
        callback=_noop,
        keybindings=kb,
    )
    if msg:
        with pytest.raises(ValueError, match=msg):
            reg.register_action_keybindings(action)
    else:
        reg.register_action_keybindings(action)


@pytest.mark.parametrize(
    "kb1, kb2, kb3",
    [
        (
            [
                {
                    "primary": KeyMod.CtrlCmd | KeyCode.KeyA,
                    "when": "active",
                    "weight": 10,
                },
            ],
            [
                {
                    "primary": KeyMod.CtrlCmd | KeyCode.KeyA,
                },
            ],
            [
                {"primary": KeyMod.CtrlCmd | KeyCode.KeyA, "weight": 5},
            ],
        ),
    ],
)
def test_register_action_keybindings_priorization(kb1: str, kb2: str, kb3: str) -> None:
    """Check `get_context_prioritized_keybinding`."""
    reg = KeyBindingsRegistry()

    action1 = Action(
        id="cmd_id1",
        title="title1",
        callback=_noop,
        keybindings=kb1,
    )
    reg.register_action_keybindings(action1)

    action2 = Action(
        id="cmd_id2",
        title="title2",
        callback=_noop,
        keybindings=kb2,
    )
    reg.register_action_keybindings(action2)

    action3 = Action(
        id="cmd_id3",
        title="title3",
        callback=_noop,
        keybindings=kb3,
    )
    reg.register_action_keybindings(action3)

    keybinding = reg.get_context_prioritized_keybinding(
        kb1[0]["primary"], {"active": False}
    )
    assert keybinding.command_id == "cmd_id3"

    keybinding = reg.get_context_prioritized_keybinding(
        kb1[0]["primary"], {"active": True}
    )
    assert keybinding.command_id == "cmd_id1"

    keybinding = reg.get_context_prioritized_keybinding(
        KeyMod.Shift | kb1[0]["primary"], {"active": True}
    )
    assert keybinding is None


@pytest.mark.parametrize(
    "kb1, kb2, gt, lt, eq",
    [
        (
            {
                "primary": KeyMod.CtrlCmd | KeyCode.KeyA,
                "command_id": "command_id1",
                "weight": 0,
                "when": None,
                "source": KeyBindingSource.USER,
            },
            {
                "primary": KeyMod.CtrlCmd | KeyCode.KeyA,
                "command_id": "command_id2",
                "weight": 0,
                "when": None,
                "source": KeyBindingSource.APP,
            },
            True,
            False,
            False,
        ),
        (
            {
                "primary": KeyMod.CtrlCmd | KeyCode.KeyA,
                "command_id": "command_id1",
                "weight": 0,
                "when": None,
                "source": KeyBindingSource.USER,
            },
            {
                "primary": KeyMod.CtrlCmd | KeyCode.KeyA,
                "command_id": "command_id2",
                "weight": 10,
                "when": None,
                "source": KeyBindingSource.APP,
            },
            True,
            False,
            False,
        ),
        (
            {
                "primary": KeyMod.CtrlCmd | KeyCode.KeyA,
                "command_id": "command_id1",
                "weight": 0,
                "when": None,
                "source": KeyBindingSource.USER,
            },
            {
                "primary": KeyMod.CtrlCmd | KeyCode.KeyA,
                "command_id": "command_id2",
                "weight": 10,
                "when": None,
                "source": KeyBindingSource.USER,
            },
            False,
            True,
            False,
        ),
        (
            {
                "primary": KeyMod.CtrlCmd | KeyCode.KeyA,
                "command_id": "command_id1",
                "weight": 10,
                "when": None,
                "source": KeyBindingSource.USER,
            },
            {
                "primary": KeyMod.CtrlCmd | KeyCode.KeyA,
                "command_id": "command_id2",
                "weight": 10,
                "when": None,
                "source": KeyBindingSource.USER,
            },
            False,
            False,
            True,
        ),
    ],
)
def test_registered_keybinding_comparison(
    kb1: dict, kb2: dict, gt: bool, lt: bool, eq: bool
) -> None:
    rkb1 = _RegisteredKeyBinding(
        keybinding=kb1["primary"],
        command_id=kb1["command_id"],
        weight=kb1["weight"],
        when=kb1["when"],
        source=kb1["source"],
    )
    rkb2 = _RegisteredKeyBinding(
        keybinding=kb2["primary"],
        command_id=kb2["command_id"],
        weight=kb2["weight"],
        when=kb2["when"],
        source=kb2["source"],
    )
    assert (rkb1 > rkb2) == gt
    assert (rkb1 < rkb2) == lt
    assert (rkb1 == rkb2) == eq
