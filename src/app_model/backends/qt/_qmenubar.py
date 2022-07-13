from typing import List, Mapping, Optional, Union

from qtpy.QtWidgets import QMenuBar, QWidget

from ... import Application
from ._qaction import QMenuItemAction
from ._qmenu import QModelMenu

try:
    from qtpy import QT6
except ImportError:
    QT6 = False


class QModelMenuBar(QMenuBar):
    """QMenuBar that is built from a list of model menu ids."""

    def __init__(
        self,
        menus: List[str],
        app: Union[str, Application],
        parent: Optional[QWidget] = None,
    ) -> None:
        super().__init__(parent)

        for menu_id in menus:
            self.addMenu(QModelMenu(menu_id, app, "File", self))

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
