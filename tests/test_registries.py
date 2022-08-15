from app_model.registries import KeyBindingsRegistry, MenusRegistry
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
