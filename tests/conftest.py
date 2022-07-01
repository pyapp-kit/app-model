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
    app = FullApp("complete_test_app")

    actions = [
        Action(
            id=Commands.OPEN,
            title="Open...",
            callback=app.mocks.open,
            menus=[{"id": Menus.FILE}],
        ),
        # putting these above undo redo to make sure that group sorting works
        Action(
            id=Commands.COPY,
            title="Copy",
            icon="fa5s.copy",
            callback=app.mocks.copy,
            menus=[{"id": Menus.EDIT, "group": "2_copy_paste"}],
        ),
        Action(
            id=Commands.PASTE,
            title="Paste",
            icon="fa5s.paste",
            callback=app.mocks.paste,
            menus=[{"id": Menus.EDIT, "group": "2_copy_paste"}],
        ),
        # putting this above UNDO to make sure that order sorting works
        Action(
            id=Commands.REDO,
            title="Redo",
            tooltip="Redo it!",
            icon="fa5s.redo",
            enablement="allow_undo_redo",
            callback=app.mocks.redo,
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
            icon="fa5s.undo",
            enablement="allow_undo_redo",
            callback=app.mocks.undo,
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
    ]
    for action in actions:
        app.register_action(action)

    try:
        yield app
    finally:
        Application.destroy("complete_test_app")
