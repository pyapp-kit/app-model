from app_model import types
from fonticon_fa6 import FA6S


class MenuId:
    FILE = "file"
    EDIT = "edit"
    HELP = "help"


ACTIONS = [
    types.Action(
        icon=FA6S.file_circle_plus,
        title="New",
        shortcut=types.StandardKeyBinding.New,
        statusTip="Create a new file",
        menus=[{'id': MenuId.FILE, 'group': '1_loadsave'}],
        callback=new_file,
    ),
    types.Action(
        icon=FA6S.folder_open,
        title="Open...",
        shortcut=types.StandardKeyBinding.Open,
        statusTip="Open an existing file",
        menus=[{'id': MenuId.FILE, 'group': '1_loadsave'}],
        callback=open_file,
    ),
    types.Action(
        icon=FA6S.floppy_disk,
        title="Save",
        shortcut=types.StandardKeyBinding.Save,
        statusTip="Save the document to disk",
        menus=[{'id': MenuId.FILE, 'group': '1_loadsave'}],
        callback=save,
    ),
    types.Action(
        title="Save As...",
        shortcut=types.StandardKeyBinding.SaveAs,
        statusTip="Save the document under a new name",
        menus=[{'id': MenuId.FILE, 'group': '1_loadsave'}],
        callback=save_as,
    ),
    types.Action(
        title="Exit",
        shortcut="Ctrl+Q",
        statusTip="Exit the application",
        menus=[{'id': MenuId.FILE, 'group': '3_launchexit'}],
        callback=close,
    ),
    types.Action(
        icon=FA6S.scissors,
        title="Cut",
        shortcut=types.StandardKeyBinding.Cut,
        statusTip="Cut the current selection's contents to the clipboard",
        menus=[{'id': MenuId.EDIT}],
        callback=cut,
    ),
    types.Action(
        icon=FA6S.copy,
        title="Copy",
        shortcut=types.StandardKeyBinding.Copy,
        statusTip="Copy the current selection's contents to the clipboard",
        menus=[{'id': MenuId.EDIT}],
        callback=copy,
    ),
    types.Action(
        icon=FA6S.paste,
        title="Paste",
        shortcut=types.StandardKeyBinding.Paste,
        statusTip="Paste the clipboard's contents into the current selection",
        menus=[{'id': MenuId.EDIT}],
        callback=paste,
    ),
    types.Action(
        title="About",
        statusTip="Show the application's About box",
        menus=[{'id': MenuId.HELP}],
        callback=about,
    ),
]

# QT specific stuff

from qtpy.QtWidgets import QMainWindow, QTextEdit
from qtpy.QtCore import QFileInfo

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self._cur_file: str = ""
        self._text_edit = QTextEdit()
        self.setCentralWidget(self._text_edit)
        self._text_edit.document().contentsChanged.connect(self.document_was_modified)

        self.set_current_file("")

    def document_was_modified(self):
        self.setWindowModified(self._text_edit.document().isModified())

    def set_current_file(self, fileName: str) -> None:
        self._cur_file = fileName
        self._text_edit.document().setModified(False)
        self.setWindowModified(False)

        if self._cur_file:
            shown_name = self.stripped_name(self._cur_file)
        else:
            shown_name = "untitled.txt"

        self.setWindowTitle(f"{shown_name}[*] - Application")

    def stripped_name(self, fullFileName: str):
        return QFileInfo(fullFileName).fileName()