from __future__ import annotations

from typing import TYPE_CHECKING, Mapping, Optional, Union

from qtpy import QT6
from qtpy.QtWidgets import QMenu

from app_model import Application
from app_model.types import SubmenuItem

from ._qaction import QMenuItemAction
from ._util import to_qicon

if TYPE_CHECKING:
    from qtpy.QtWidgets import QWidget

    from app_model.types import MenuIdStr


class QModelMenu(QMenu):
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
        menu_id: MenuIdStr,
        app: Union[str, Application],
        title: Optional[str] = None,
        parent: Optional[QWidget] = None,
    ):
        assert isinstance(menu_id, str), f"Expected str, got {type(menu_id)!r}"
        self._menu_id = menu_id
        super().__init__(parent)
        self._app = Application.get_or_create(app) if isinstance(app, str) else app
        self.setObjectName(menu_id)
        if title is not None:
            self.setTitle(title)
        self.rebuild()

    def rebuild(self) -> None:
        """Rebuild menu by looking up self._menu_id in menu_registry."""
        self.clear()

        groups = list(self._app.menus.iter_menu_groups(self._menu_id))
        n_groups = len(groups)
        for n, group in enumerate(groups):
            for item in group:
                if isinstance(item, SubmenuItem):
                    submenu = QModelSubmenu(item, self._app, self)
                    self.addMenu(submenu)
                else:
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
