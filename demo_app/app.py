from app_model import Application
from app_model.backends.qt import QModelMainWindow

from .actions import ACTIONS
from .constants import MenuId


class MyApp(Application):
    def __init__(self) -> None:
        super().__init__("my_application")

        # ACTIONS is a list of Action objects.
        for action in ACTIONS:
            self.register_action(action)

        self._main_window = QModelMainWindow(app=self)
        # This will build a menu bar based on these menus
        self._main_window.setModelMenuBar([MenuId.FILE, MenuId.EDIT])

    def show(self) -> None:
        """Show the app"""
        self._main_window.show()
