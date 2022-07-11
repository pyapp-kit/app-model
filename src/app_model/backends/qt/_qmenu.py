from __future__ import annotations

from typing import (
    TYPE_CHECKING,
    Callable,
    Collection,
    Mapping,
    Optional,
    Protocol,
    Set,
    Union,
)

from qtpy import QT6
from qtpy.QtWidgets import QMenu, QToolBar, QWidget
from qtpy.QtCore import QObject

from app_model import Application
from app_model.types import SubmenuItem

from ._qaction import QMenuItemAction
from ._util import to_qicon

if TYPE_CHECKING:
    from qtpy.QtWidgets import QAction, QWidget

# fmt: off
class _AcceptsMenus(Protocol):
    _app: Application
    def clear(self) -> None: ...
    def addMenu(self, menu: QMenu): ...
    def addAction(self, menu: QAction): ...
    def addSeparator(self): ...

# fmt: on


class _MenuMixin(QObject):
    _app: Application
    _menu_id: str

    def __init__(
        self,
        menu_id: str,
        app: Union[str, Application],
    ):
        assert isinstance(menu_id, str), f"Expected str, got {type(menu_id)!r}"
        self._menu_id = menu_id
        self._app = Application.get_or_create(app) if isinstance(app, str) else app
        self.setObjectName(menu_id)
        self.rebuild()
        self._app.menus.menus_changed.connect(self._on_registry_changed)
        self.destroyed.connect(self._disconnect)

    def _disconnect(self) -> None:
        self._app.menus.menus_changed.disconnect(self._on_registry_changed)

    def _on_registry_changed(self, changed_ids: Set[str]) -> None:
        if self._menu_id in changed_ids:
            self.rebuild()

    def rebuild(
        self: _AcceptsMenus,
        include_submenus=True,
        exclude: Optional[Collection[str]] = None,
    ) -> None:
        """Rebuild menu by looking up self._menu_id in menu_registry."""
        self.clear()
        _exclude = exclude or set()

        groups = list(self._app.menus.iter_menu_groups(self._menu_id))
        n_groups = len(groups)
        for n, group in enumerate(groups):
            for item in group:
                if isinstance(item, SubmenuItem) and include_submenus:
                    submenu = QModelSubmenu(item, self._app, parent=self)
                    self.addMenu(submenu)
                elif item.command.id not in _exclude:
                    action = QMenuItemAction(item, app=self._app, parent=self)
                    self.addAction(action)
            if n < n_groups - 1:
                self.addSeparator()

    def update_from_context(
        self, ctx: Mapping[str, object], _recurse: bool = True
    ) -> None:
        """Update the enabled/visible state of each menu item with `ctx`.

        See `app_model.expressions` for details on expressions.

        Parameters
        ----------
        ctx : Mapping
            A namepsace that will be used to `eval()` the `'enablement'` and
            `'when'` expressions provided for each action in the menu.
            *ALL variables used in these expressions must either be present in
            the `ctx` dict, or be builtins*.
        _recurse : bool
            recursion check, internal use only
        """
        for action in self.actions():
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


class QModelMenu(QMenu, _MenuMixin):
    """QMenu for a menu_id in an `app_model` MenusRegistry.

    Parameters
    ----------
    menu_id : str
        Menu ID to look up in the registry.
    app : Union[str, Application]
        Application instance or name of application instance.
    parent : Optional[QWidget]
        Optional parent widget, by default None
    """

    def __init__(
        self,
        menu_id: str,
        app: Union[str, Application],
        title: Optional[str] = None,
        parent: Optional[QWidget] = None,
    ):
        QMenu.__init__(self, parent)
        _MenuMixin.__init__(self, menu_id, app)
        if title is not None:
            self.setTitle(title)

    def findAction(self, object_name: str) -> Union[QAction, QModelMenu, None]:
        """Find an action by its ObjectName.

        Parameters
        ----------
        object_name : str
            Action ID to find. Note that `QCommandAction` have `ObjectName` set
            to their `command.id`
        """
        return next((a for a in self.actions() if a.objectName() == object_name), None)


class QModelSubmenu(QModelMenu):
    """QMenu for a menu_id in an `app_model` MenusRegistry.

    Parameters
    ----------
    submenu : SubmenuItem
        SubmenuItem for which to create a QMenu.
    app : Union[str, Application]
        Application instance or name of application instance.
    parent : Optional[QWidget]
        Optional parent widget, by default None
    """

    def __init__(
        self,
        submenu: SubmenuItem,
        app: Union[str, Application],
        parent: Optional[QWidget] = None,
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
        super().update_from_context(ctx)
        self.setEnabled(expr.eval(ctx) if (expr := self._submenu.enablement) else True)
        # TODO: ... visibility needs to be controlled at the level of placement
        # in the submenu.  consider only using the `when` expression
        # self.setVisible(expr.eval(ctx) if (expr := self._submenu.when) else True)


class QModelToolBar(QToolBar, _MenuMixin):
    """QToolBar that is built from a list of model menu ids."""

    def __init__(
        self,
        menu_id: str,
        app: Union[str, Application],
        *,
        exclude: Optional[Collection[str]] = None,
        title: Optional[str] = None,
        parent: Optional[QWidget] = None,
    ) -> None:
        self._exclude = exclude
        QToolBar.__init__(self, parent)
        _MenuMixin.__init__(self, menu_id, app)
        if title is not None:
            self.setWindowTitle(title)

    def rebuild(self, include_submenus=False) -> None:
        super().rebuild(include_submenus=include_submenus, exclude=self._exclude)

    def addMenu(self, menu: QMenu):
        pass
