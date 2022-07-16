import pytest

from app_model.registries import CommandsRegistry, KeyBindingsRegistry, MenusRegistry
from app_model.types import MenuItem


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


def test_commands_registry() -> None:
    reg = CommandsRegistry()
    reg.register_command("my.id", lambda: None, "My Title")
    assert "(1 commands)" in repr(reg)
    assert "my.id" in str(reg)

    with pytest.raises(ValueError, match="Command 'my.id' already registered"):
        reg.register_command("my.id", lambda: None, "My Title")


def test_commands_raises() -> None:
    reg = CommandsRegistry(raise_synchronous_exceptions=True)

    def raise_exc() -> None:
        raise RuntimeError("boom")

    reg.register_command("my.id", raise_exc, "My Title")

    with pytest.raises(RuntimeError, match="boom"):
        reg.execute_command("my.id")
