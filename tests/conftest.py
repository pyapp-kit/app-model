from unittest.mock import Mock

import pytest

from app_model import Action, Application


class Menus:
    FILE = "file"
    EDIT = "edit"
    HELP = "help"


class Commands:
    OPEN = "open"
    UNDO = "undo"
    REDO = "redo"
    COPY = "copy"
    PASTE = "paste"


class Mocks:
    def __init__(self) -> None:
        self.open = Mock(name=Commands.OPEN)
        self.undo = Mock(name=Commands.UNDO)
        self.redo = Mock(name=Commands.REDO)
        self.copy = Mock(name=Commands.COPY)
        self.paste = Mock(name=Commands.PASTE)


class FullApp(Application):
    Menus = Menus
    Commands = Commands

    def __init__(self, name: str) -> None:
        super().__init__(name)
        self.mocks = Mocks()


@pytest.fixture
def full_app() -> Application:
    """Premade application."""
    app = FullApp("test_app")

    actions = [
        Action(
            id=Commands.OPEN,
            title="Open...",
            callback=app.mocks.open,
            menus=[{"id": Menus.FILE}],
        ),
        Action(
            id=Commands.UNDO,
            title="Undo",
            callback=app.mocks.undo,
            menus=[{"id": Menus.EDIT, "group": "1_undo_redo", "order": 0}],
        ),
        Action(
            id=Commands.REDO,
            title="Redo",
            callback=app.mocks.redo,
            menus=[{"id": Menus.EDIT, "group": "1_undo_redo", "order": 0}],
        ),
        Action(
            id=Commands.COPY,
            title="Copy",
            callback=app.mocks.copy,
            menus=[{"id": Menus.EDIT, "group": "2_copy_paste"}],
        ),
        Action(
            id=Commands.PASTE,
            title="Paste",
            callback=app.mocks.paste,
            menus=[{"id": Menus.EDIT, "group": "2_copy_paste"}],
        ),
    ]
    for action in actions:
        app.register_action(action)

    yield app

    Application.destroy("test_app")
