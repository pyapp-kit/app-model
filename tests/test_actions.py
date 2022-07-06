from unittest.mock import Mock

import pytest

from app_model import Application
from app_model.registries import register_action
from app_model.types import Action

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
    dict(add_to_command_palette=False),
]


@pytest.fixture
def app():
    app = Application("test")
    app.commands_changed = Mock()
    app.commands.registered.connect(app.commands_changed)
    app.keybindings_changed = Mock()
    app.keybindings.registered.connect(app.keybindings_changed)
    app.menus_changed = Mock()
    app.menus.menus_changed.connect(app.menus_changed)
    yield app
    Application.destroy("test")
    assert "test" not in Application._instances


@pytest.mark.parametrize("kwargs", KWARGS)
@pytest.mark.parametrize("mode", ["str", "decorator", "action"])
def test_register_action_decorator(kwargs, app: Application, mode):
    # make sure mocks are working
    assert not list(app.commands)
    assert not list(app.keybindings)
    assert not list(app.menus)

    cmd_id = "cmd.id"
    kwargs["title"] = "Test title"

    # register the action
    if mode == "decorator":

        @register_action(app=app, id_or_action=cmd_id, **kwargs)
        def f1():
            return "hi"

        assert f1() == "hi"  # decorator returns the function

    else:

        def f2():
            return "hi"

        if mode == "str":
            register_action(app=app, id_or_action=cmd_id, callback=f2, **kwargs)

        elif mode == "action":
            action = Action(id=cmd_id, callback=f2, **kwargs)
            app.register_action(action)

    # make sure the command is registered
    assert cmd_id in app.commands
    assert list(app.commands)
    # make sure an event was emitted signaling the command was registered
    app.commands_changed.assert_called_once_with(cmd_id)  # type: ignore

    # make sure we can call the command, and that we can inject dependencies.
    assert app.commands.execute_command(cmd_id).result() == "hi"

    # make sure menus are registered if specified
    menus = kwargs.get("menus", [])
    if menus := kwargs.get("menus"):
        for entry in menus:
            assert entry["id"] in app.menus
            app.menus_changed.assert_any_call({entry["id"]})
    else:
        menus = list(app.menus)
        if kwargs.get("add_to_command_palette") is not False:
            assert app.menus.COMMAND_PALETTE_ID in app.menus
            assert len(menus) == 1
        else:
            assert not list(app.menus)

    # make sure keybindings are registered if specified
    if keybindings := kwargs.get("keybindings"):
        for entry in keybindings:
            key = PRIMARY_KEY if len(entry) == 1 else OS_KEY  # see KWARGS[5]
            assert any(i.keybinding == key for i in app.keybindings)
            app.keybindings_changed.assert_called()  # type: ignore
    else:
        assert not list(app.keybindings)

    # check that calling the dispose function removes everything.
    app.dispose()
    assert not list(app.commands)
    assert not list(app.keybindings)
    assert not list(app.menus)


def test_errors(app: Application):
    with pytest.raises(ValueError, match="'title' is required"):
        app.register_action("cmd_id")  # type: ignore
    with pytest.raises(TypeError, match="must be a string or an Action"):
        app.register_action(None)  # type: ignore
