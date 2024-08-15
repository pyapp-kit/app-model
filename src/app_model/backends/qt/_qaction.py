from __future__ import annotations

import contextlib
from typing import TYPE_CHECKING, ClassVar, Mapping
from weakref import WeakValueDictionary

from app_model import Application
from app_model.expressions import Expr
from app_model.types import ToggleRule

from ._qkeymap import QKeyBindingSequence
from ._util import to_qicon

if TYPE_CHECKING:
    from PyQt6.QtGui import QAction
    from qtpy.QtCore import QObject
    from typing_extensions import Self

    from app_model.types import CommandRule, MenuItem
else:
    from qtpy.QtWidgets import QAction


class QCommandAction(QAction):
    """Base QAction for a command id. Can execute the command.

    Parameters
    ----------
    command_id : str
        Command ID.
    app : Application | str
        Application instance or name of application instance.
    parent : QObject | None
        Optional parent widget, by default None
    """

    def __init__(
        self,
        command_id: str,
        app: Application | str,
        parent: QObject | None = None,
    ):
        super().__init__(parent)
        self._app = Application.get_or_create(app) if isinstance(app, str) else app
        self._command_id = command_id
        self.setObjectName(command_id)
        self._keybinding_tooltip = ""
        if kb := self._app.keybindings.get_keybinding(command_id):
            self.setShortcut(QKeyBindingSequence(kb.keybinding))
            self._keybinding_tooltip = f"({kb.keybinding.to_text()})"
        self.triggered.connect(self._on_triggered)

    def _on_triggered(self, checked: bool) -> None:
        # execute_command returns a Future, for the sake of eventually being
        # asynchronous without breaking the API.  For now, we call result()
        # to raise any exceptions.
        self._app.commands.execute_command(self._command_id).result()


class QCommandRuleAction(QCommandAction):
    """QAction for a CommandRule.

    Parameters
    ----------
    command_rule : CommandRule
        `CommandRule` instance to create an action for.
    app : Application | str
        Application instance or name of application instance.
    parent : QObject | None
        Optional parent widget, by default None
    use_short_title : bool
        If True, use the `short_title` of the command rule, if it exists.
    """

    def __init__(
        self,
        command_rule: CommandRule,
        app: Application | str,
        parent: QObject | None = None,
        *,
        use_short_title: bool = False,
    ):
        super().__init__(command_rule.id, app, parent)
        self._cmd_rule = command_rule
        if use_short_title and command_rule.short_title:
            self.setText(command_rule.short_title)  # pragma: no cover
        else:
            self.setText(command_rule.title)
        if command_rule.icon:
            self.setIcon(to_qicon(command_rule.icon))
        self.setIconVisibleInMenu(command_rule.icon_visible_in_menu)
        if command_rule.tooltip:
            self.setToolTip(command_rule.tooltip)
        if command_rule.status_tip:
            self.setStatusTip(command_rule.status_tip)
        if command_rule.toggled is not None:
            self.setCheckable(True)
            self._refresh()
        tooltip_with_keybinding = (
            f"{self.toolTip()} {self._keybinding_tooltip}".rstrip()
        )
        self.setToolTip(tooltip_with_keybinding)

    def update_from_context(self, ctx: Mapping[str, object]) -> None:
        """Update the enabled state of this menu item from `ctx`."""
        self.setEnabled(expr.eval(ctx) if (expr := self._cmd_rule.enablement) else True)
        if expr2 := self._cmd_rule.toggled:
            if (
                isinstance(expr2, Expr)
                or isinstance(expr2, ToggleRule)
                and (expr2 := expr2.condition)
            ):
                self.setChecked(expr2.eval(ctx))

    def _refresh(self) -> None:
        if isinstance(self._cmd_rule.toggled, ToggleRule):
            if get_current := self._cmd_rule.toggled.get_current:
                _current = self._app.injection_store.inject(
                    get_current, on_unresolved_required_args="ignore"
                )
                self.setChecked(_current())


class QMenuItemAction(QCommandRuleAction):
    """QAction for a MenuItem.

    Mostly the same as a `CommandRuleAction`, but aware of the `menu_item.when` clause
    to toggle visibility.

    Parameters
    ----------
    menu_item : MenuItem
        `MenuItem` instance to create an action for.
    app : Application | str
        Application instance or name of application instance.
    parent : QObject | None
        Optional parent widget, by default None
    """

    _cache: ClassVar[WeakValueDictionary[tuple[int, int], QMenuItemAction]] = (
        WeakValueDictionary()
    )

    def __init__(
        self,
        menu_item: MenuItem,
        app: Application | str,
        parent: QObject | None = None,
    ):
        super().__init__(menu_item.command, app, parent)
        self._menu_item = menu_item
        with contextlib.suppress(NameError):
            self.update_from_context(self._app.context)

    @staticmethod
    def _cache_key(app: Application, menu_item: MenuItem) -> tuple[int, int]:
        return (id(app), hash(menu_item))

    @classmethod
    def create(
        cls,
        menu_item: MenuItem,
        app: Application | str,
        parent: QObject | None = None,
    ) -> Self:
        """Create a new QMenuItemAction for the given menu item.

        Prefer this method over `__init__` to ensure that the cache is used,
        so that:

        ```python
        a1 = QMenuItemAction.create(action, full_app)
        a2 = QMenuItemAction.create(action, full_app)
        a1 is a2  # True
        ```
        """
        app = Application.get_or_create(app) if isinstance(app, str) else app
        cache_key = QMenuItemAction._cache_key(app, menu_item)
        if cache_key in cls._cache:
            res = cls._cache[cache_key]
            res.setParent(parent)
            return res

        cls._cache[cache_key] = obj = cls(menu_item, app, parent)
        return obj

    def update_from_context(self, ctx: Mapping[str, object]) -> None:
        """Update the enabled/visible state of this menu item from `ctx`."""
        super().update_from_context(ctx)
        self.setVisible(expr.eval(ctx) if (expr := self._menu_item.when) else True)

    def __repr__(self) -> str:
        name = self.__class__.__name__
        return f"{name}({self._menu_item!r}, app={self._app.name!r})"
