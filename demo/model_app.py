from pathlib import Path
from typing import List

from qtpy.QtCore import QFile, QFileInfo, QSaveFile, Qt, QTextStream
from qtpy.QtWidgets import QApplication, QFileDialog, QMessageBox, QTextEdit

from app_model import Application, types
from app_model.backends.qt import QModelMainWindow
from app_model.expressions import create_context


class MainWindow(QModelMainWindow):
    def __init__(self, app: Application):
        super().__init__(app)

        self._cur_file: str = ""
        self._text_edit = QTextEdit()
        self._text_edit.copyAvailable.connect(self._update_context)

        self.setCentralWidget(self._text_edit)
        self.setModelMenuBar([MenuId.FILE, MenuId.EDIT, MenuId.HELP])
        self.addModelToolBar(MenuId.FILE, exclude={CommandId.SAVE_AS, CommandId.EXIT})
        self.addModelToolBar(MenuId.EDIT)
        self.addModelToolBar(MenuId.HELP)
        self.statusBar().showMessage("Ready")

        self.set_current_file("")

        self._ctx = create_context(self)
        self._ctx.changed.connect(self._on_context_changed)
        self._ctx["copyAvailable"] = False

    def _update_context(self, available: bool) -> None:
        self._ctx["copyAvailable"] = available

    def _on_context_changed(self) -> None:
        self.menuBar().update_from_context(self._ctx)

    def set_current_file(self, fileName: str) -> None:
        self._cur_file = fileName
        self._text_edit.document().setModified(False)
        self.setWindowModified(False)

        if self._cur_file:
            shown_name = QFileInfo(self._cur_file).fileName()
        else:
            shown_name = "untitled.txt"

        self.setWindowTitle(f"{shown_name}[*] - Application")

    def save(self) -> bool:
        return self.save_file(self._cur_file) if self._cur_file else self.save_as()

    def save_as(self) -> bool:
        fileName, _ = QFileDialog.getSaveFileName(self)
        if fileName:
            return self.save_file(fileName)
        return False

    def save_file(self, fileName: str) -> bool:
        error = None
        QApplication.setOverrideCursor(Qt.WaitCursor)
        file = QSaveFile(fileName)
        if file.open(QFile.OpenModeFlag.WriteOnly | QFile.OpenModeFlag.Text):  # type: ignore
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
        return True

    def maybe_save(self) -> bool:
        if self._text_edit.document().isModified():
            ret = QMessageBox.warning(
                self,
                "Application",
                "The document has been modified.\nDo you want to save " "your changes?",
                QMessageBox.StandardButton.Save  # type: ignore
                | QMessageBox.StandardButton.Discard
                | QMessageBox.StandardButton.Cancel,
            )
            if ret == QMessageBox.StandardButton.Save:
                return self.save()
            elif ret == QMessageBox.StandardButton.Cancel:
                return False
        return True

    def new_file(self) -> None:
        if self.maybe_save():
            self._text_edit.clear()
            self.set_current_file("")

    def open_file(self) -> None:
        if self.maybe_save():
            fileName, _ = QFileDialog.getOpenFileName(self)
            if fileName:
                self.load_file(fileName)

    def load_file(self, fileName: str) -> None:
        file = QFile(fileName)
        if not file.open(QFile.OpenModeFlag.ReadOnly | QFile.OpenModeFlag.Text):  # type: ignore
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

    def about(self) -> None:
        QMessageBox.about(
            self,
            "About Application",
            "The <b>Application</b> example demonstrates how to write "
            "modern GUI applications using Qt, with a menu bar, "
            "toolbars, and a status bar.",
        )

    def cut(self) -> None:
        self._text_edit.cut()

    def copy(self) -> None:
        self._text_edit.copy()

    def paste(self) -> None:
        self._text_edit.paste()

    def close(self) -> bool:
        return super().close()


# Actions defined declaratively outside of QMainWindow class ...
# menus and toolbars will be made and added automatically


class MenuId:
    FILE = "file"
    EDIT = "edit"
    HELP = "help"


class CommandId:
    SAVE_AS = "save_file_as"
    EXIT = "exit"


ABOUT_ICON_PATH = Path(__file__).parent / "images" / "about.svg"

ACTIONS: List[types.Action] = [
    types.Action(
        id="new_file",
        icon="fa6-solid:file-circle-plus",
        title="New",
        keybindings=[types.StandardKeyBinding.New],
        status_tip="Create a new file",
        menus=[{"id": MenuId.FILE, "group": "1_loadsave"}],
        callback=MainWindow.new_file,
    ),
    types.Action(
        id="open_file",
        icon="fa6-solid:folder-open",
        title="Open...",
        keybindings=[types.StandardKeyBinding.Open],
        status_tip="Open an existing file",
        menus=[{"id": MenuId.FILE, "group": "1_loadsave"}],
        callback=MainWindow.open_file,
    ),
    types.Action(
        id="save_file",
        icon="fa6-solid:floppy-disk",
        title="Save",
        keybindings=[types.StandardKeyBinding.Save],
        status_tip="Save the document to disk",
        menus=[{"id": MenuId.FILE, "group": "1_loadsave"}],
        callback=MainWindow.save,
    ),
    types.Action(
        id=CommandId.SAVE_AS,
        title="Save As...",
        keybindings=[types.StandardKeyBinding.SaveAs],
        status_tip="Save the document under a new name",
        menus=[{"id": MenuId.FILE, "group": "1_loadsave"}],
        callback=MainWindow.save_as,
    ),
    types.Action(
        id=CommandId.EXIT,
        title="Exit",
        keybindings=[types.StandardKeyBinding.Quit],
        status_tip="Exit the application",
        menus=[{"id": MenuId.FILE, "group": "3_launchexit"}],
        callback=MainWindow.close,
    ),
    types.Action(
        id="cut",
        icon="fa6-solid:scissors",
        title="Cut",
        keybindings=[types.StandardKeyBinding.Cut],
        enablement="copyAvailable",
        status_tip="Cut the current selection's contents to the clipboard",
        menus=[{"id": MenuId.EDIT}],
        callback=MainWindow.cut,
    ),
    types.Action(
        id="copy",
        icon="fa6-solid:copy",
        title="Copy",
        keybindings=[types.StandardKeyBinding.Copy],
        enablement="copyAvailable",
        status_tip="Copy the current selection's contents to the clipboard",
        menus=[{"id": MenuId.EDIT}],
        callback=MainWindow.copy,
    ),
    types.Action(
        id="paste",
        icon="fa6-solid:paste",
        title="Paste",
        keybindings=[types.StandardKeyBinding.Paste],
        status_tip="Paste the clipboard's contents into the current selection",
        menus=[{"id": MenuId.EDIT}],
        callback=MainWindow.paste,
    ),
    types.Action(
        id="about",
        icon=f"file:///{ABOUT_ICON_PATH}",
        title="About",
        status_tip="Show the application's About box",
        menus=[{"id": MenuId.HELP}],
        callback=MainWindow.about,
    ),
]


# Main setup

if __name__ == "__main__":
    app = Application(name="my_app")
    for action in ACTIONS:
        app.register_action(action)
    qapp = QApplication.instance() or QApplication([])
    qapp.setAttribute(Qt.ApplicationAttribute.AA_DontShowIconsInMenus)
    main_win = MainWindow(app=app)

    app.injection_store.register_provider(lambda: main_win, MainWindow)
    main_win.show()
    qapp.exec_()
