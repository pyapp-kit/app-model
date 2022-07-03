import sys
from pathlib import Path
from unittest.mock import Mock

import pytest

from app_model import Action, Application
from app_model.types import KeyCode, KeyMod, SubmenuItem

try:
    from fonticon_fa5 import FA5S

    UNDO_ICON = FA5S.undo
except ImportError:
    UNDO_ICON = "fa5s.undo"

FIXTURES = Path(__file__).parent / "fixtures"


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
    UNIMPORTABLE = "unimportable"
    NOT_CALLABLE = "not.callable"
    RAISES = "raises.error"


def _raise_an_error():
    raise ValueError("This is an error")


class Mocks:
    def __init__(self) -> None:
        self.open = Mock(name=Commands.OPEN)
        self.undo = Mock(name=Commands.UNDO)
        self.copy = Mock(name=Commands.COPY)
        self.paste = Mock(name=Commands.PASTE)
        self.open_from_a = Mock(name=Commands.OPEN_FROM_A)
        self.open_from_b = Mock(name=Commands.OPEN_FROM_B)

    @property
    def redo(self) -> Mock:
        """This tests that we can lazily import a callback.

        There is a function called `run_me` in fixtures/fake_module.py that calls the
        global mock in that module.  In the redo action below, we declare:
        `callback="fake_module:run_me"`

        So, whenever the redo action is triggered, it should import that module, and
        then call the mock.  We can also access it here at `mocks.redo`... but the
        fixtures directory must be added to sys path during the test (as we do below)
        """
        try:
            from fake_module import GLOBAL_MOCK  # noqa

            return GLOBAL_MOCK
        except ImportError as e:
            raise ImportError(
                "This mock must be run with the fixutres directory added to sys.path."
            ) from e


class FullApp(Application):
    Menus = Menus
    Commands = Commands

    def __init__(self, name: str) -> None:
        super().__init__(name)
        self.mocks = Mocks()


def build_app(name: str = "complete_test_app") -> FullApp:
    app = FullApp(name)
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
            callback="fake_module:run_me",  # this is a function in fixtures
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
        Action(
            id=Commands.UNIMPORTABLE,
            title="Can't be found",
            callback="unresolvable:function",
        ),
        Action(
            id=Commands.NOT_CALLABLE,
            title="Will Never Work",
            callback="fake_module:attr",
        ),
        Action(
            id=Commands.RAISES,
            title="Will raise an error",
            callback=_raise_an_error,
        ),
    ]
    for action in actions:
        app.register_action(action)

    return app


@pytest.fixture
def full_app(monkeypatch) -> Application:
    """Premade application."""
    try:
        app = build_app()
        with monkeypatch.context() as m:
            # mock path to add fake_module
            m.setattr(sys, "path", [str(FIXTURES)] + sys.path)
            # make sure it's not already in sys.modules
            sys.modules.pop("fake_module", None)
            yield app
            # clear the global mock if it's been called
            app.mocks.redo.reset_mock()
    finally:
        Application.destroy("complete_test_app")
