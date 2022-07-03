from unittest.mock import Mock

import pytest

from app_model import Action, Application
from app_model.types import KeyCode, KeyMod, SubmenuItem

try:
    from fonticon_fa5 import FA5S

    UNDO_ICON = FA5S.undo
except ImportError:
    UNDO_ICON = "fa5s.undo"


class Menus:
    FILE = "file"
    EDIT = "edit"
    HELP = "help"
    FILE_OPEN_FROM = "file/open_from"


class Commands:
    OPEN = "open"
    UNDO = "undo"
    REDO = "redo"
    COPY = "copy"
    PASTE = "paste"
    OPEN_FROM_A = "open.from_a"
    OPEN_FROM_B = "open.from_b"


class Mocks:
    def __init__(self) -> None:
        self.open = Mock(name=Commands.OPEN, side_effect=lambda: print("open"))
        self.undo = Mock(name=Commands.UNDO, side_effect=lambda: print("undo"))
        self.redo = Mock(name=Commands.REDO, side_effect=lambda: print("redo"))
        self.copy = Mock(name=Commands.COPY, side_effect=lambda: print("copy"))
        self.paste = Mock(name=Commands.PASTE, side_effect=lambda: print("paste"))
        self.open_from_a = Mock(name=Commands.OPEN_FROM_A)
        self.open_from_b = Mock(name=Commands.OPEN_FROM_B)


class FullApp(Application):
    Menus = Menus
    Commands = Commands

    def __init__(self, name: str) -> None:
        super().__init__(name)
        self.mocks = Mocks()


def build_app() -> Application:
    app = FullApp("complete_test_app")
    app.menus.append_menu_items(
        [
            (
                Menus.FILE,
                SubmenuItem(
                    submenu=Menus.FILE_OPEN_FROM,
                    title="Open From...",
                    icon="fa5s.folder-open",
                    when="not something_open",
                    enablement="friday",
                ),
            )
        ]
    )

    actions = [
        Action(
            id=Commands.OPEN,
            title="Open...",
            callback=app.mocks.open,
            menus=[{"id": Menus.FILE}],
            keybindings=[{"primary": "Ctrl+O"}],
        ),
        # putting these above undo redo to make sure that group sorting works
        Action(
            id=Commands.COPY,
            title="Copy",
            icon="fa5s.copy",
            callback=app.mocks.copy,
            menus=[{"id": Menus.EDIT, "group": "2_copy_paste"}],
            keybindings=[{"primary": KeyMod.CtrlCmd | KeyCode.KeyC}],
        ),
        Action(
            id=Commands.PASTE,
            title="Paste",
            icon="fa5s.paste",
            callback=app.mocks.paste,
            menus=[{"id": Menus.EDIT, "group": "2_copy_paste"}],
            keybindings=[{"primary": "Ctrl+V", "mac": "Cmd+V"}],
        ),
        # putting this above UNDO to make sure that order sorting works
        Action(
            id=Commands.REDO,
            title="Redo",
            tooltip="Redo it!",
            icon="fa5s.redo",
            enablement="allow_undo_redo",
            callback=app.mocks.redo,
            keybindings=[{"primary": "Ctrl+Shift+Z"}],
            menus=[
                {
                    "id": Menus.EDIT,
                    "group": "1_undo_redo",
                    "order": 1,
                    "when": "not something_to_undo",
                }
            ],
        ),
        Action(
            id=Commands.UNDO,
            tooltip="Undo it!",
            title="Undo",
            icon=UNDO_ICON,  # testing alternate way to specify icon
            enablement="allow_undo_redo",
            callback=app.mocks.undo,
            keybindings=[{"primary": "Ctrl+Z"}],
            menus=[
                {
                    "id": Menus.EDIT,
                    "group": "1_undo_redo",
                    "order": 0,
                    "when": "something_to_undo",
                }
            ],
        ),
        # test the navigation key
        Action(
            id=Commands.OPEN,
            title="AtTop",
            callback=app.mocks.open,
            menus=[{"id": Menus.EDIT, "group": "navigation"}],
        ),
        # test submenus
        Action(
            id=Commands.OPEN_FROM_A,
            title="Open from A",
            callback=app.mocks.open_from_a,
            menus=[{"id": Menus.FILE_OPEN_FROM}],
        ),
        Action(
            id=Commands.OPEN_FROM_B,
            title="Open from B",
            callback=app.mocks.open_from_b,
            menus=[{"id": Menus.FILE_OPEN_FROM}],
        ),
    ]
    for action in actions:
        app.register_action(action)

    return app


@pytest.fixture
def full_app() -> Application:
    """Premade application."""
    app = build_app()
    try:
        yield app
    finally:
        Application.destroy("complete_test_app")
