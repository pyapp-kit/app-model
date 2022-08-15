from qtpy.QtGui import QKeySequence

from app_model.backends.qt import QModelKeyBindingEdit
from app_model.types import KeyBinding, KeyCode, KeyMod


def test_qkeysequenceedit(qtbot):
    edit = QModelKeyBindingEdit()
    qtbot.addWidget(edit)
    assert edit.keyBinding() is None
    edit.setKeySequence(QKeySequence("Shift+A"))
    assert edit.keyBinding() == KeyBinding(parts=[KeyMod.Shift | KeyCode.KeyA])
