# Copyright (C) 2013 Riverbank Computing Limited.
# Copyright (C) 2022 The Qt Company Ltd.
# SPDX-License-Identifier: LicenseRef-Qt-Commercial OR BSD-3-Clause

from fonticon_fa6 import FA6S
from qtpy.QtCore import QFile, QFileInfo, QSaveFile, Qt, QTextStream
from qtpy.QtGui import QKeySequence
from qtpy.QtWidgets import (
    QAction,
    QApplication,
    QFileDialog,
    QMainWindow,
    QMessageBox,
    QTextEdit,
)
from superqt import fonticon


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self._cur_file = ""

        self._text_edit = QTextEdit()
        self.setCentralWidget(self._text_edit)

        self.create_actions()
        self.create_menus()
        self.create_tool_bars()
        self.create_status_bar()

        self.set_current_file("")

    def new_file(self):
        if self.maybe_save():
            self._text_edit.clear()
            self.set_current_file("")

    def open(self):
        if self.maybe_save():
            fileName, filtr = QFileDialog.getOpenFileName(self)
            if fileName:
                self.load_file(fileName)

    def save(self):
        return self.save_file(self._cur_file) if self._cur_file else self.save_as()

    def save_as(self):
        fileName, filtr = QFileDialog.getSaveFileName(self)
        if fileName:
            return self.save_file(fileName)

        return False

    def about(self):
        QMessageBox.about(
            self,
            "About Application",
            "The <b>Application</b> example demonstrates how to write "
            "modern GUI applications using Qt, with a menu bar, "
            "toolbars, and a status bar.",
        )

    def create_actions(self):
        self._new_act = QAction(
            fonticon.icon(FA6S.file_circle_plus),
            "&New",
            self,
            shortcut=QKeySequence.StandardKey.New,
            statusTip="Create a new file",
            triggered=self.new_file,
        )

        self._open_act = QAction(
            fonticon.icon(FA6S.folder_open),
            "&Open...",
            self,
            shortcut=QKeySequence.StandardKey.Open,
            statusTip="Open an existing file",
            triggered=self.open,
        )

        self._save_act = QAction(
            fonticon.icon(FA6S.floppy_disk),
            "&Save",
            self,
            shortcut=QKeySequence.StandardKey.Save,
            statusTip="Save the document to disk",
            triggered=self.save,
        )

        self._save_as_act = QAction(
            "Save &As...",
            self,
            shortcut=QKeySequence.StandardKey.SaveAs,
            statusTip="Save the document under a new name",
            triggered=self.save_as,
        )

        self._exit_act = QAction(
            "E&xit",
            self,
            shortcut="Ctrl+Q",
            statusTip="Exit the application",
            triggered=self.close,
        )

        self._cut_act = QAction(
            fonticon.icon(FA6S.scissors),
            "Cu&t",
            self,
            shortcut=QKeySequence.StandardKey.Cut,
            statusTip="Cut the current selection's contents to the clipboard",
            triggered=self._text_edit.cut,
        )

        self._copy_act = QAction(
            fonticon.icon(FA6S.copy),
            "&Copy",
            self,
            shortcut=QKeySequence.StandardKey.Copy,
            statusTip="Copy the current selection's contents to the clipboard",
            triggered=self._text_edit.copy,
        )

        self._paste_act = QAction(
            fonticon.icon(FA6S.paste),
            "&Paste",
            self,
            shortcut=QKeySequence.StandardKey.Paste,
            statusTip="Paste the clipboard's contents into the current selection",
            triggered=self._text_edit.paste,
        )

        self._about_act = QAction(
            "&About",
            self,
            statusTip="Show the application's About box",
            triggered=self.about,
        )

        self._cut_act.setEnabled(False)
        self._copy_act.setEnabled(False)
        self._text_edit.copyAvailable.connect(self._cut_act.setEnabled)
        self._text_edit.copyAvailable.connect(self._copy_act.setEnabled)

    def create_menus(self):
        self._file_menu = self.menuBar().addMenu("&File")
        self._file_menu.addAction(self._new_act)
        self._file_menu.addAction(self._open_act)
        self._file_menu.addAction(self._save_act)
        self._file_menu.addAction(self._save_as_act)
        self._file_menu.addSeparator()
        self._file_menu.addAction(self._exit_act)

        self._edit_menu = self.menuBar().addMenu("&Edit")
        self._edit_menu.addAction(self._cut_act)
        self._edit_menu.addAction(self._copy_act)
        self._edit_menu.addAction(self._paste_act)

        self.menuBar().addSeparator()

        self._help_menu = self.menuBar().addMenu("&Help")
        self._help_menu.addAction(self._about_act)

    def create_tool_bars(self):
        self._file_tool_bar = self.addToolBar("File")
        self._file_tool_bar.addAction(self._new_act)
        self._file_tool_bar.addAction(self._open_act)
        self._file_tool_bar.addAction(self._save_act)

        self._edit_tool_bar = self.addToolBar("Edit")
        self._edit_tool_bar.addAction(self._cut_act)
        self._edit_tool_bar.addAction(self._copy_act)
        self._edit_tool_bar.addAction(self._paste_act)

    def create_status_bar(self):
        self.statusBar().showMessage("Ready")

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

        self.set_current_file(fileName)
        self.statusBar().showMessage("File saved", 2000)
        return True

    def set_current_file(self, fileName: str):
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


if __name__ == "__main__":
    qapp = QApplication.instance() or QApplication([])
    qapp.setAttribute(Qt.ApplicationAttribute.AA_DontShowIconsInMenus)
    main_win = MainWindow()
    main_win.show()
    qapp.exec_()
