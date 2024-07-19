import pytest

from app_model.registries import KeyBindingsRegistry, MenusRegistry
from app_model.types import (
    Action,
    KeyBinding,
    KeyBindingRule,
    KeyCode,
    KeyMod,
    MenuItem,
)


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
        reg.filter_keybinding = "string"


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
def test_register_action_keybindings_filter(kb, msg) -> None:
    """Check `filter_keybinding` in `register_action_keybindings`."""
    reg = KeyBindingsRegistry()
    reg.filter_keybinding = _filter_fun

    action = Action(
        id="cmd_id1",
        title="title1",
        callback=lambda: None,
        keybindings=kb,
    )
    if msg:
        with pytest.raises(ValueError, match=msg):
            reg.register_action_keybindings(action)
    else:
        reg.register_action_keybindings(action)
