from typing import TYPE_CHECKING
from unittest.mock import Mock

from app_model.backends.qt import QCommandRuleAction, QMenuItemAction
from app_model.types import Action, MenuItem, ToggleRule

if TYPE_CHECKING:
    from qtpy.QtWidgets import QAction

    from app_model import Application
    from conftest import FullApp


def test_cache_qaction(qapp, full_app: "FullApp") -> None:
    action = next(
        i for k, items in full_app.menus for i in items if isinstance(i, MenuItem)
    )
    a1 = QMenuItemAction(action, full_app)
    a2 = QMenuItemAction(action, full_app)
    assert a1 is a2
    assert repr(a1).startswith("QMenuItemAction")


def test_toggle_qaction(qapp, simple_app: "Application") -> None:
    mock = Mock()
    x = False

    def _connect(qaction: "QAction") -> None:
        qaction.toggled.connect(mock)

    def _toggle() -> None:
        nonlocal x
        x = not x

    action = Action(
        id="test.toggle",
        title="Test toggle",
        toggled=ToggleRule(initialize=lambda: x, experimental_connect=_connect),
        callback=_toggle,
    )
    simple_app.register_action(action)

    a1 = QCommandRuleAction(action, simple_app)
    assert a1.isCheckable()
    assert not a1.isChecked()

    a1.trigger()
    assert a1.isChecked()
    assert x
    mock.assert_called_once_with(True)
    mock.reset_mock()

    a1.trigger()
    assert not a1.isChecked()
    assert not x
    mock.assert_called_once_with(False)
