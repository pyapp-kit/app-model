from qtpy.QtWidgets import QApplication, QFileDialog


def open_file():
    name, _ = QFileDialog.getOpenFileName()
    print("Open file:", name)


def close():
    if win := QApplication.activeWindow():
        win.close()
    print("close")


def undo():
    print("undo")


def redo():
    print("redo")


def cut():
    print("cut")


def copy():
    print("copy")


def paste():
    print("paste")
