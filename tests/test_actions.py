from typing import Callable, Optional
from unittest.mock import Mock, patch

import pytest

from app_model import (
    Action,
    CommandsRegistry,
    KeybindingsRegistry,
    MenusRegistry,
    register_action,
)
from app_model._types import CommandIdStr

PRIMARY_KEY = "ctrl+a"
OS_KEY = "ctrl+b"
MENUID = "some.menu.id"
KWARGS = [
    {},
    dict(enablement="x == 1"),
    dict(menus=[{"id": MENUID}]),
    dict(enablement="3 >= 1", menus=[{"id": MENUID}]),
    dict(keybindings=[{"primary": PRIMARY_KEY}]),
    dict(
        keybindings=[
            {"primary": PRIMARY_KEY, "mac": OS_KEY, "win": OS_KEY, "linux": OS_KEY}
        ]
    ),
    dict(keybindings=[{"primary": "ctrl+a"}], menus=[{"id": MENUID}]),
]


@pytest.fixture
def cmd_reg():
    reg = CommandsRegistry()
    reg.registered_emit = Mock()
    reg.registered.connect(reg.registered_emit)
    with patch.object(CommandsRegistry, "instance", return_value=reg):
        yield reg
    reg._commands.clear()


@pytest.fixture
def key_reg():
    reg = KeybindingsRegistry()
    reg.registered_emit = Mock()
    reg.registered.connect(reg.registered_emit)
    with patch.object(KeybindingsRegistry, "instance", return_value=reg):
        yield reg
    reg._coreKeybindings.clear()


@pytest.fixture
def menu_reg():
    reg = MenusRegistry()
    reg.menus_changed_emit = Mock()
    reg.menus_changed.connect(reg.menus_changed_emit)
    with patch.object(MenusRegistry, "instance", return_value=reg):
        yield reg
    reg._menu_items.clear()


@pytest.mark.parametrize("kwargs", KWARGS)
@pytest.mark.parametrize("mode", ["str", "decorator", "action"])
def test_register_action_decorator(
    kwargs,
    cmd_reg: CommandsRegistry,
    key_reg: KeybindingsRegistry,
    menu_reg: MenusRegistry,
    mode,
):
    # make sure mocks are working
    assert not list(cmd_reg)
    assert not list(key_reg)
    assert not list(menu_reg)

    dispose: Optional[Callable] = None
    cmd_id = CommandIdStr("cmd.id")
    kwargs["title"] = "Test title"

    # register the action
    if mode == "decorator":

        @register_action(cmd_id, **kwargs)
        def f1():
            return "hi"

        assert f1() == "hi"  # decorator returns the function

    else:

        def f2():
            return "hi"

        if mode == "str":
            dispose = register_action(cmd_id, run=f2, **kwargs)

        elif mode == "action":
            action = Action(id=cmd_id, run=f2, **kwargs)
            dispose = register_action(action)

    # make sure the command is registered
    assert cmd_id in cmd_reg
    assert list(cmd_reg)
    # make sure an event was emitted signaling the command was registered
    cmd_reg.registered_emit.assert_called_once_with(cmd_id)  # type: ignore

    # make sure we can call the command, and that we can inject dependencies.
    assert cmd_reg.execute_command(cmd_id).result() == "hi"

    # make sure menus are registered if specified
    if menus := kwargs.get("menus"):
        for entry in menus:
            assert entry["id"] in menu_reg
            menu_reg.menus_changed_emit.assert_called_with({entry["id"]})
    else:
        assert not list(menu_reg)

    # make sure keybindings are registered if specified
    if keybindings := kwargs.get("keybindings"):
        for entry in keybindings:
            key = PRIMARY_KEY if len(entry) == 1 else OS_KEY  # see KWARGS[5]
            assert any(i.keybinding == key for i in key_reg)
            key_reg.registered_emit.assert_called()  # type: ignore
    else:
        assert not list(key_reg)

    # if we're not using the decorator, check that calling the dispose
    # function removes everything.  (the decorator returns the function, so can't
    # return the dispose function)
    if dispose:
        dispose()
        assert not list(cmd_reg)
        assert not list(key_reg)
        assert not list(menu_reg)


def test_errors():
    with pytest.raises(ValueError, match="'title' is required"):
        register_action("cmd_id")  # type: ignore
    with pytest.raises(TypeError, match="must be a string or an Action"):
        register_action(None)  # type: ignore


def test_instances():
    assert isinstance(MenusRegistry().instance(), MenusRegistry)
    assert isinstance(
        KeybindingsRegistry().instance(),
        KeybindingsRegistry,
    )
    assert isinstance(CommandsRegistry().instance(), CommandsRegistry)
