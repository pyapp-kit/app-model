import pytest

from app_model.registries import KeyBindingsRegistry, MenusRegistry
from app_model.types import KeyBinding, KeyBindingRule, KeyCode, KeyMod, MenuItem


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


def test_register_keybinding_rule_filter() -> None:
    """Check `filter_keybinding` in `register_keybinding_rule`."""
    reg = KeyBindingsRegistry()

    def filter_fun(kb: KeyBinding) -> str | None:
        print(f"is mod: {kb.part0.is_modifier_key()}")
        if kb.part0.is_modifier_key():
            return "modifier only sequences not allowed"
        return ""

    reg.filter_keybinding = filter_fun
    # Valid keybinding
    kb = KeyBindingRule(primary=KeyMod.CtrlCmd | KeyCode.KeyO)
    reg.register_keybinding_rule("test", kb)
    # Invalid keybinding
    kb = KeyBindingRule(primary=KeyMod.CtrlCmd | KeyMod.Shift)
    with pytest.raises(ValueError, match="modifier only"):
        reg.register_keybinding_rule("test", kb)
