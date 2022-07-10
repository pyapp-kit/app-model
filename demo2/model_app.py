from app_model import types, Application
from fonticon_fa6 import FA6S

from app_model.backends.qt import QModelMainWindow
from qtpy.QtWidgets import QTextEdit, QApplication, QMessageBox, QFileDialog
from qtpy.QtCore import QFile, QFileInfo, QSaveFile, QTextStream, Qt


class MenuId:
    FILE = "file"
    EDIT = "edit"
    HELP = "help"


def new_file(win: "MainWindow"):
    win.new_file()


def open_file(win: "MainWindow"):
    win.open_file()


def save(win: "MainWindow"):
    win.save()


def save_as(win: "MainWindow"):
    win.save_as()


def close(win: "MainWindow"):
    win.close()


def cut(win: "MainWindow"):
    win._text_edit.cut()


def copy(win: "MainWindow"):
    win._text_edit.copy()


def paste(win: "MainWindow"):
    win._text_edit.paste()


def about(win: "MainWindow"):
    win.about()



class MainWindow(QModelMainWindow):
    def __init__(self, app: Application):
        super().__init__(app)

        self._cur_file: str = ""
        self._text_edit = QTextEdit()
        self.setCentralWidget(self._text_edit)
        self.setModelMenuBar([MenuId.FILE, MenuId.EDIT, MenuId.HELP])

        self.set_current_file("")

    def set_current_file(self, fileName: str) -> None:
        self._cur_file = fileName
        self._text_edit.document().setModified(False)
        self.setWindowModified(False)

        if self._cur_file:
            shown_name = QFileInfo(self._cur_file).fileName()
        else:
            shown_name = "untitled.txt"

        self.setWindowTitle(f"{shown_name}[*] - Application")

    def save(self):
        return self.save_file(self._cur_file) if self._cur_file else self.save_as()

    def save_as(self):
        fileName, filtr = QFileDialog.getSaveFileName(self)
        if fileName:
            return self.save_file(fileName)

        return False

    def save_file(self, fileName):
        error = None
        QApplication.setOverrideCursor(Qt.WaitCursor)
        file = QSaveFile(fileName)
        if file.open(QFile.OpenModeFlag.WriteOnly | QFile.OpenModeFlag.Text):
            outf = QTextStream(file)
            outf << self._text_edit.toPlainText()
            if not file.commit():
                reason = file.errorString()
                error = f"Cannot write file {fileName}:\n{reason}."
        else:
            reason = file.errorString()
            error = f"Cannot open file {fileName}:\n{reason}."
        QApplication.restoreOverrideCursor()

        if error:
            QMessageBox.warning(self, "Application", error)
            return False

    def maybe_save(self):
        if self._text_edit.document().isModified():
            ret = QMessageBox.warning(
                self,
                "Application",
                "The document has been modified.\nDo you want to save " "your changes?",
                QMessageBox.StandardButton.Save
                | QMessageBox.StandardButton.Discard
                | QMessageBox.StandardButton.Cancel,
            )
            if ret == QMessageBox.StandardButton.Save:
                return self.save()
            elif ret == QMessageBox.StandardButton.Cancel:
                return False
        return True

    def new_file(self):
        if self.maybe_save():
            self._text_edit.clear()
            self.set_current_file("")

    def open_file(self):
        if self.maybe_save():
            fileName, _ = QFileDialog.getOpenFileName(self)
            if fileName:
                self.load_file(fileName)

    def load_file(self, fileName):
        file = QFile(fileName)
        if not file.open(QFile.OpenModeFlag.ReadOnly | QFile.OpenModeFlag.Text):
            reason = file.errorString()
            QMessageBox.warning(
                self, "Application", f"Cannot read file {fileName}:\n{reason}."
            )
            return

        inf = QTextStream(file)
        QApplication.setOverrideCursor(Qt.WaitCursor)
        self._text_edit.setPlainText(inf.readAll())
        QApplication.restoreOverrideCursor()

        self.set_current_file(fileName)
        self.statusBar().showMessage("File loaded", 2000)

    def about(self):
        QMessageBox.about(
            self,
            "About Application",
            "The <b>Application</b> example demonstrates how to write "
            "modern GUI applications using Qt, with a menu bar, "
            "toolbars, and a status bar.",
        )


ACTIONS = [
    types.Action(
        id="new_file",
        icon=FA6S.file_circle_plus,
        title="New",
        keybindings=[types.StandardKeyBinding.New],
        status_tip="Create a new file",
        menus=[{"id": MenuId.FILE, "group": "1_loadsave"}],
        callback=new_file,
    ),
    types.Action(
        id="open_file",
        icon=FA6S.folder_open,
        title="Open...",
        keybindings=[types.StandardKeyBinding.Open],
        status_tip="Open an existing file",
        menus=[{"id": MenuId.FILE, "group": "1_loadsave"}],
        callback=MainWindow.open_file,
    ),
    types.Action(
        id="save_file",
        icon=FA6S.floppy_disk,
        title="Save",
        keybindings=[types.StandardKeyBinding.Save],
        status_tip="Save the document to disk",
        menus=[{"id": MenuId.FILE, "group": "1_loadsave"}],
        callback=save,
    ),
    types.Action(
        id="save_file_as",
        title="Save As...",
        keybindings=[types.StandardKeyBinding.SaveAs],
        status_tip="Save the document under a new name",
        menus=[{"id": MenuId.FILE, "group": "1_loadsave"}],
        callback=save_as,
    ),
    types.Action(
        id="close",
        title="Exit",
        keybindings=[types.StandardKeyBinding.Quit],
        status_tip="Exit the application",
        menus=[{"id": MenuId.FILE, "group": "3_launchexit"}],
        callback=close,
    ),
    types.Action(
        id="cut",
        icon=FA6S.scissors,
        title="Cut",
        keybindings=[types.StandardKeyBinding.Cut],
        enablement="copyAvailable",
        status_tip="Cut the current selection's contents to the clipboard",
        menus=[{"id": MenuId.EDIT}],
        callback=cut,
    ),
    types.Action(
        id="copy",
        icon=FA6S.copy,
        title="Copy",
        keybindings=[types.StandardKeyBinding.Copy],
        enablement="copyAvailable",
        status_tip="Copy the current selection's contents to the clipboard",
        menus=[{"id": MenuId.EDIT}],
        callback=copy,
    ),
    types.Action(
        id="paste",
        icon=FA6S.paste,
        title="Paste",
        keybindings=[types.StandardKeyBinding.Paste],
        status_tip="Paste the clipboard's contents into the current selection",
        menus=[{"id": MenuId.EDIT}],
        callback=paste,
    ),
    types.Action(
        id="about",
        title="About",
        status_tip="Show the application's About box",
        menus=[{"id": MenuId.HELP}],
        callback=about,
    ),
]


# Main setup

if __name__ == "__main__":
    app = Application(name="my_app")
    for action in ACTIONS:
        app.register_action(action)
    qapp = QApplication([])
    qapp.setAttribute(Qt.ApplicationAttribute.AA_DontShowIconsInMenus)
    main_win = MainWindow(app=app)

    app.injection_store.register_provider(lambda: main_win, MainWindow)
    main_win.show()
    qapp.exec_()
