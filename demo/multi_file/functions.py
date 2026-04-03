from qtpy.QtWidgets import QApplication, QFileDialog


def open_file() -> None:
    name, _ = QFileDialog.getOpenFileName()
    print("Open file:", name)


def close() -> None:
    if win := QApplication.activeWindow():
        win.close()
    print("close")


def undo() -> None:
    print("undo")


def redo() -> None:
    print("redo")


def cut() -> None:
    print("cut")


def copy() -> None:
    print("copy")


def paste() -> None:
    print("paste")
