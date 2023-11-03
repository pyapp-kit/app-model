from typing import List

import pytest

from app_model import Application
from app_model.registries import register_action
from app_model.types import Action, KeyBinding

PRIMARY_KEY = "ctrl+a"
OS_KEY = "ctrl+b"
MENUID = "some.menu.id"
KWARGS = [
    {},
    {"enablement": "x == 1"},
    {"menus": [MENUID]},  # test that we can pass menus as a single string too
    {"enablement": "3 >= 1", "menus": [{"id": MENUID}]},
    {"keybindings": [{"primary": PRIMARY_KEY}]},
    {
        "keybindings": [
            {"primary": PRIMARY_KEY, "mac": OS_KEY, "win": OS_KEY, "linux": OS_KEY}
        ]
    },
    {"keybindings": [{"primary": "ctrl+a"}], "menus": [{"id": MENUID}]},
    {"palette": False},
]


@pytest.mark.parametrize("kwargs", KWARGS)
@pytest.mark.parametrize("mode", ["str", "decorator", "action"])
def test_register_action_decorator(
    kwargs: dict, simple_app: Application, mode: str
) -> None:
    # make sure mocks are working
    app = simple_app
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
            id_ = entry if isinstance(entry, str) else entry["id"]
            assert id_ in app.menus
            app.menus_changed.assert_any_call({id_})
    else:
        menus = list(app.menus)
        if kwargs.get("palette") is not False:
            assert app.menus.COMMAND_PALETTE_ID in app.menus
            assert len(menus) == 1
        else:
            assert not list(app.menus)

    # make sure keybindings are registered if specified
    if keybindings := kwargs.get("keybindings"):
        for entry in keybindings:
            key = PRIMARY_KEY if len(entry) == 1 else OS_KEY  # see KWARGS[5]
            key = KeyBinding.from_str(key)
            assert any(i.keybinding == key for i in app.keybindings)
            app.keybindings_changed.assert_called()  # type: ignore
    else:
        assert not list(app.keybindings)

    # check that calling the dispose function removes everything.
    app.dispose()
    assert not list(app.commands)
    assert not list(app.keybindings)
    assert not list(app.menus)


def test_errors(simple_app: Application):
    with pytest.raises(ValueError, match="'title' is required"):
        simple_app.register_action("cmd_id")  # type: ignore
    with pytest.raises(TypeError, match="must be a string or an Action"):
        simple_app.register_action(None)  # type: ignore


def test_register_multiple_actions(simple_app: Application):
    actions: List[Action] = [
        Action(id="cmd_id1", title="title1", callback=lambda: None),
        Action(id="cmd_id2", title="title2", callback=lambda: None),
    ]
    dispose = simple_app.register_actions(actions)
    assert len(simple_app.commands) == 2
    dispose()
    assert not list(simple_app.commands)
