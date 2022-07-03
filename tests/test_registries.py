from app_model.registries import CommandsRegistry, KeyBindingsRegistry, MenusRegistry
from app_model.types import MenuItem


def test_menus_registry():
    reg = MenusRegistry()
    reg.append_menu_items([("file", {"command": {"id": "file.new", "title": "File"}})])
    reg.append_menu_items([("file.sub", {"submenu": "Sub", "title": "SubTitle"})])

    assert isinstance(reg.get_menu("file")[0], MenuItem)
    assert "(2 menus)" in repr(reg)
    assert "File" in str(reg)
    assert "Sub" in str(reg)  # ok to change


def test_keybindings_registry():
    reg = KeyBindingsRegistry()
    assert "(0 bindings)" in repr(reg)


def test_commands_registry():
    reg = CommandsRegistry()
    reg.register_command("my.id", lambda: None, "My Title")
    assert "(1 commands)" in repr(reg)
    assert "my.id" in str(reg)
