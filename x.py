from qtpy.QtWidgets import QApplication

from app_model import Action, Application
from app_model.backends.qt import QModelMainWindow

app = Application("my-app")
app.register_actions(
    [
        Action(
            id="action1", title="Action 1", menus=["File"], callback=lambda: print("1")
        ),
        Action(
            id="action2",
            title="Action 2",
            icon="fa6-solid:eye",
            menus=["Edit"],
            callback=lambda: print("2"),
        ),
        Action(
            id="action3",
            title="Action 3",
            icon="fa6-solid:plus",
            menus=["View"],
            icon_visible_in_menu=False,
            callback=lambda: print("3"),
        ),
    ]
)

qapp = QApplication([])

win = QModelMainWindow(app)
win.setModelMenuBar(app.menus)
win.addModelToolBar("Edit")
win.addModelToolBar("View")
win.show()

qapp.exec()
