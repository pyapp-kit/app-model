from typing import TYPE_CHECKING
from unittest.mock import Mock

from app_model.backends.qt import QCommandRuleAction, QMenuItemAction
from app_model.types import Action, CommandRule, MenuItem, ToggleRule

if TYPE_CHECKING:
    from app_model import Application
    from conftest import FullApp


def test_cache_qaction(qapp, full_app: "FullApp") -> None:
    action = next(
        i for k, items in full_app.menus for i in items if isinstance(i, MenuItem)
    )
    a1 = QMenuItemAction.create(action, full_app)
    a2 = QMenuItemAction.create(action, full_app)
    assert a1 is a2
    assert repr(a1).startswith("QMenuItemAction")


def test_toggle_qaction(qapp, simple_app: "Application") -> None:
    mock = Mock()
    x = False

    def current() -> bool:
        mock()
        return x

    def _toggle() -> None:
        nonlocal x
        x = not x

    action = Action(
        id="test.toggle",
        title="Test toggle",
        toggled=ToggleRule(get_current=current),
        callback=_toggle,
    )
    simple_app.register_action(action)

    a1 = QCommandRuleAction(action, simple_app)
    mock.assert_called_once()
    mock.reset_mock()

    assert a1.isCheckable()
    assert not a1.isChecked()

    a1.trigger()
    assert a1.isChecked()
    assert x

    a1.trigger()
    assert not a1.isChecked()
    assert not x

    x = True
    a1._refresh()
    mock.assert_called_once()
    assert a1.isChecked()


def test_icon_visible_in_menu(qapp, simple_app: "Application") -> None:
    rule = CommandRule(id="test", title="Test", icon_visible_in_menu=False)
    q_action = QCommandRuleAction(command_rule=rule, app=simple_app)
    assert not q_action.isIconVisibleInMenu()
