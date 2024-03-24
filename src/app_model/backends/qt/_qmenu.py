from __future__ import annotations

import contextlib
from typing import TYPE_CHECKING, Collection, Iterable, Mapping, Sequence, cast

from qtpy.QtWidgets import QMenu, QMenuBar, QToolBar

from app_model import Application
from app_model.types import SubmenuItem

from ._qaction import QCommandRuleAction, QMenuItemAction
from ._util import to_qicon

try:
    from qtpy import QT6
except ImportError:
    QT6 = False

if TYPE_CHECKING:
    from qtpy.QtWidgets import QAction, QWidget


class QModelMenu(QMenu):
    """QMenu for a menu_id in an `app_model` MenusRegistry.

    Parameters
    ----------
    menu_id : str
        Menu ID to look up in the registry.
    app : Application | str
        Application instance or name of application instance.
    title : str | None
        Optional title for the menu, by default None
    parent : QWidget | None
        Optional parent widget, by default None
    """

    def __init__(
        self,
        menu_id: str,
        app: Application | str,
        title: str | None = None,
        parent: QWidget | None = None,
    ):
        QMenu.__init__(self, parent)

        # NOTE: code duplication with QModelToolBar, but Qt mixins and multiple
        # inheritance are problematic for some versions of Qt, and for typing
        assert isinstance(menu_id, str), f"Expected str, got {type(menu_id)!r}"
        self._menu_id = menu_id
        self._app = Application.get_or_create(app) if isinstance(app, str) else app
        self.setObjectName(menu_id)
        self.rebuild()
        self._app.menus.menus_changed.connect(self._on_registry_changed)
        self.destroyed.connect(self._disconnect)
        # ----------------------

        if title is not None:
            self.setTitle(title)
        self.aboutToShow.connect(self._on_about_to_show)

    def findAction(self, object_name: str) -> QAction | QModelMenu | None:
        """Find an action by its ObjectName.

        Parameters
        ----------
        object_name : str
            Action ID to find. Note that `QCommandAction` have `ObjectName` set
            to their `command.id`
        """
        return _find_action(self.actions(), object_name)

    def update_from_context(
        self, ctx: Mapping[str, object], _recurse: bool = True
    ) -> None:
        """Update the enabled/visible state of each menu item with `ctx`.

        See `app_model.expressions` for details on expressions.

        Parameters
        ----------
        ctx : Mapping
            A namespace that will be used to `eval()` the `'enablement'` and
            `'when'` expressions provided for each action in the menu.
            *ALL variables used in these expressions must either be present in
            the `ctx` dict, or be builtins*.
        _recurse : bool
            recursion check, internal use only
        """
        _update_from_context(self.actions(), ctx, _recurse=_recurse)

    def rebuild(
        self, include_submenus: bool = True, exclude: Collection[str] | None = None
    ) -> None:
        """Rebuild menu by looking up self._menu_id in menu_registry."""
        _rebuild(
            menu=self,
            app=self._app,
            menu_id=self._menu_id,
            include_submenus=include_submenus,
            exclude=exclude,
        )

    def _on_about_to_show(self) -> None:
        for action in self.actions():
            if isinstance(action, QCommandRuleAction):
                action._refresh()

    def _disconnect(self) -> None:
        self._app.menus.menus_changed.disconnect(self._on_registry_changed)

    def _on_registry_changed(self, changed_ids: set[str]) -> None:
        if self._menu_id in changed_ids:
            # if this (sub)menu has been removed from the registry,
            # we may hit a RuntimeError when trying to rebuild it.
            with contextlib.suppress(RuntimeError):
                self.rebuild()


class QModelSubmenu(QModelMenu):
    """QMenu for a menu_id in an `app_model` MenusRegistry.

    Parameters
    ----------
    submenu : SubmenuItem
        SubmenuItem for which to create a QMenu.
    app : Application | str
        Application instance or name of application instance.
    parent : QWidget | None
        Optional parent widget, by default None
    """

    def __init__(
        self,
        submenu: SubmenuItem,
        app: Application | str,
        parent: QWidget | None = None,
    ):
        assert isinstance(submenu, SubmenuItem), f"Expected str, got {type(submenu)!r}"
        self._submenu = submenu
        super().__init__(
            menu_id=submenu.submenu, app=app, title=submenu.title, parent=parent
        )
        if submenu.icon:
            self.setIcon(to_qicon(submenu.icon))

    def update_from_context(
        self, ctx: Mapping[str, object], _recurse: bool = True
    ) -> None:
        """Update the enabled state of this menu item from `ctx`."""
        super().update_from_context(ctx, _recurse=_recurse)
        self.setEnabled(expr.eval(ctx) if (expr := self._submenu.enablement) else True)
        # TODO: ... visibility needs to be controlled at the level of placement
        # in the submenu.  consider only using the `when` expression
        # self.setVisible(expr.eval(ctx) if (expr := self._submenu.when) else True)


class QModelToolBar(QToolBar):
    """QToolBar that is built from a list of model menu ids.

    Parameters
    ----------
    menu_id : str
        Menu ID to look up in the registry.
    app : Application | str
        Application instance or name of application instance.
    exclude : Collection[str] | None
        Optional list of menu ids to exclude from the toolbar, by default None
    title : str | None
        Optional title for the menu, by default None
    parent : QWidget | None
        Optional parent widget, by default None
    """

    def __init__(
        self,
        menu_id: str,
        app: Application | str,
        *,
        exclude: Collection[str] | None = None,
        title: str | None = None,
        parent: QWidget | None = None,
    ) -> None:
        self._exclude = exclude
        QToolBar.__init__(self, parent)

        # NOTE: code duplication with QModelMenu, but Qt mixins and multiple
        # inheritance are problematic for some versions of Qt, and for typing
        assert isinstance(menu_id, str), f"Expected str, got {type(menu_id)!r}"
        self._menu_id = menu_id
        self._app = Application.get_or_create(app) if isinstance(app, str) else app
        self.setObjectName(menu_id)
        self.rebuild()
        self._app.menus.menus_changed.connect(self._on_registry_changed)
        self.destroyed.connect(self._disconnect)
        # ----------------------

        if title is not None:
            self.setWindowTitle(title)

    def addMenu(self, menu: QMenu) -> None:
        """No-op for toolbar."""

    def findAction(self, object_name: str) -> QAction | QModelMenu | None:
        """Find an action by its ObjectName.

        Parameters
        ----------
        object_name : str
            Action ID to find. Note that `QCommandAction` have `ObjectName` set
            to their `command.id`
        """
        return _find_action(self.actions(), object_name)

    def update_from_context(
        self, ctx: Mapping[str, object], _recurse: bool = True
    ) -> None:
        """Update the enabled/visible state of each menu item with `ctx`.

        See `app_model.expressions` for details on expressions.

        Parameters
        ----------
        ctx : Mapping
            A namespace that will be used to `eval()` the `'enablement'` and
            `'when'` expressions provided for each action in the menu.
            *ALL variables used in these expressions must either be present in
            the `ctx` dict, or be builtins*.
        _recurse : bool
            recursion check, internal use only
        """
        _update_from_context(self.actions(), ctx, _recurse=_recurse)

    def rebuild(
        self, include_submenus: bool = True, exclude: Collection[str] | None = None
    ) -> None:
        """Rebuild toolbar by looking up self._menu_id in menu_registry."""
        _rebuild(
            menu=self,
            app=self._app,
            menu_id=self._menu_id,
            include_submenus=include_submenus,
            exclude=self._exclude if exclude is None else exclude,
        )

    def _disconnect(self) -> None:
        self._app.menus.menus_changed.disconnect(self._on_registry_changed)

    def _on_registry_changed(self, changed_ids: set[str]) -> None:
        if self._menu_id in changed_ids:
            self.rebuild()


class QModelMenuBar(QMenuBar):
    """QMenuBar that is built from a list of model menu ids.

    Parameters
    ----------
    menus : Mapping[str, str] | Sequence[str | tuple[str, str]]
        A mapping of menu ids to menu titles or a sequence of menu ids.
    app : Application | str
        Application instance or name of application instance.
    parent : QWidget | None
        Optional parent widget, by default None
    """

    def __init__(
        self,
        menus: Mapping[str, str] | Sequence[str | tuple[str, str]],
        app: Application | str,
        parent: QWidget | None = None,
    ) -> None:
        super().__init__(parent)

        menu_items = menus.items() if isinstance(menus, Mapping) else menus
        for item in menu_items:
            id_, title = item if isinstance(item, tuple) else (item, item.title())
            self.addMenu(QModelMenu(id_, app, title, self))

    def update_from_context(
        self, ctx: Mapping[str, object], _recurse: bool = True
    ) -> None:
        """Update the enabled/visible state of each menu item with `ctx`.

        See `app_model.expressions` for details on expressions.

        Parameters
        ----------
        ctx : Mapping
            A namespace that will be used to `eval()` the `'enablement'` and
            `'when'` expressions provided for each action in the menu.
            *ALL variables used in these expressions must either be present in
            the `ctx` dict, or be builtins*.
        _recurse : bool
            recursion check, internal use only
        """
        _update_from_context(self.actions(), ctx, _recurse=_recurse)


def _rebuild(
    menu: QMenu | QToolBar,
    app: Application,
    menu_id: str,
    include_submenus: bool = True,
    exclude: Collection[str] | None = None,
) -> None:
    """Rebuild menu by looking up `menu` in `Application`'s menu_registry."""
    actions = menu.actions()
    for action in actions:
        menu.removeAction(action)

    _exclude = exclude or set()

    groups = list(app.menus.iter_menu_groups(menu_id))
    n_groups = len(groups)
    for n, group in enumerate(groups):
        for item in group:
            if isinstance(item, SubmenuItem):
                if include_submenus:
                    submenu = QModelSubmenu(item, app, parent=menu)
                    cast("QMenu", menu).addMenu(submenu)
            elif item.command.id not in _exclude:
                action = QMenuItemAction.create(item, app=app, parent=menu)
                menu.addAction(action)
        if n < n_groups - 1:
            menu.addSeparator()


def _update_from_context(
    actions: Iterable[QAction], ctx: Mapping[str, object], _recurse: bool = True
) -> None:
    """Update the enabled/visible state of each menu item with `ctx`.

    See `app_model.expressions` for details on expressions.

    Parameters
    ----------
    actions : Iterable[QAction]
        Actions to update.
    ctx : Mapping
        A namespace that will be used to `eval()` the `'enablement'` and
        `'when'` expressions provided for each action in the menu.
        *ALL variables used in these expressions must either be present in
        the `ctx` dict, or be builtins*.
    _recurse : bool
        recursion check, internal use only
    """
    for action in actions:
        if isinstance(action, QMenuItemAction):
            action.update_from_context(ctx)
        elif not QT6 and isinstance(menu := action.menu(), QModelMenu):
            menu.update_from_context(ctx)
        elif isinstance(parent := action.parent(), QModelMenu):
            # FIXME: this is a hack for Qt6 that I don't entirely understand.
            # QAction has lost the `.menu()` method, and it's a bit hard to find
            # how to get to the parent menu now. Checking parent() seems to work,
            # but I'm not sure if it's the right thing to do, and it leads to a
            # recursion error.  I stop it with the _recurse flag here, but I wonder
            # whether that will cause other problems.
            if _recurse:
                parent.update_from_context(ctx, _recurse=False)


def _find_action(actions: Iterable[QAction], object_name: str) -> QAction | None:
    return next((a for a in actions if a.objectName() == object_name), None)
