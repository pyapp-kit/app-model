from __future__ import annotations

from typing import TYPE_CHECKING, Any, List, Mapping, Optional, Union, overload

from qtpy.QtCore import QTimer
from qtpy.QtWidgets import QMenu

from app_model import Application
from app_model.types import MenuItem, SubmenuItem

from ._qaction import QMenuItemAction

if TYPE_CHECKING:
    from qtpy.QtCore import QPoint
    from qtpy.QtWidgets import QAction, QWidget

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
        parent: Optional[QWidget] = None,
    ):
        super().__init__(parent)
        self._app = Application.get_or_create(app) if isinstance(app, str) else app

        self._menu_id = menu_id
        self._submenu_item: Optional[SubmenuItem] = None
        self._submenus: List[QModelMenu] = []
        self.rebuild()

    def rebuild(self) -> None:
        """Rebuild menu by looking up self._menu_id in menu_registry."""
        self.clear()

        groups = list(self._app.menus.iter_menu_groups(self._menu_id))
        n_groups = len(groups)

        for n, group in enumerate(groups):
            for item in group:
                if isinstance(item, SubmenuItem):
                    self.addSubmenu(item)
                else:
                    action = QMenuItemAction(item, app=self._app, parent=self)
                    self.addAction(action)
            if n < n_groups:
                self.addSeparator()

    def addSubmenu(self, submenu: SubmenuItem) -> None:
        """Add submenu to menu.

        Parameters
        ----------
        submenu : SubmenuItem
            types.SubmenuItem instance to add to menu.
        """
        sub = QModelMenu(submenu.submenu, self._app, parent=self)
        sub.setTitle(submenu.title)
        # if item.icon:
        #     sub.setIcon(to_qicon(item.icon))
        self.addMenu(sub)
        self._submenus.append(sub)  # save pointer

    def update_from_context(self, ctx: Mapping[str, object]) -> None:
        """Update the enabled/visible state of each menu item with `ctx`.

        See `app_model.expressions` for details on expressions.

        Parameters
        ----------
        ctx : Mapping
            A namepsace that will be used to `eval()` the `'enablement'` and
            `'when'` expressions provided for each action in the menu.
            *ALL variables used in these expressions must either be present in
            the `ctx` dict, or be builtins*.
        """
        for action in self.actions():
            if isinstance(action, QMenuItemAction):
                action.update_from_context(ctx)
            elif (menu := action.menu()) and isinstance(menu, QModelMenu):
                menu.update_from_context(ctx)

    @overload
    def exec(self) -> Optional[QAction]:  # noqa: D102
        ...

    @overload
    def exec(self, pos: QPoint, action: Optional[QAction] = ...) -> Optional[QAction]:
        ...

    def exec(self, *args: Any, **kwargs: Any) -> Optional[QAction]:
        """Execute the menu synchronously, and return the action that was selected."""
        if action := super().exec_(*args, **kwargs):
            if isinstance(item := action.data(), MenuItem):

                def _cb() -> None:
                    self._app.commands.execute_command(item.command.id)

                QTimer.singleShot(0, _cb)
            return action
        return None
