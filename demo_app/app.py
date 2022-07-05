from app_model import Application
from app_model.backends.qt import QModelMenu
from qtpy.QtWidgets import QMainWindow
from .actions import ACTIONS
from .constants import MenuId


class MyApp(Application):
    def __init__(self) -> None:
        super().__init__("my_application")

        for action in ACTIONS:
            self.register_action(action)

        self._main_window = QMainWindow()
        for menu_id in [MenuId.FILE, MenuId.EDIT]:
            menu = QModelMenu(menu_id, self, "File", self._main_window)
            self._main_window.menuBar().addMenu(menu)

    def show(self):
        self._main_window.show()

