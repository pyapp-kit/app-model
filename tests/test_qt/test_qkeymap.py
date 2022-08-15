from qtpy.QtCore import Qt
from qtpy.QtGui import QKeySequence

from app_model.backends.qt import qkey2modelkey, qkeysequence2modelkeybinding
from app_model.types import KeyBinding, KeyCode, KeyCombo, KeyMod

# stuff we don't know how to deal with yet


def test_qkey_lookup() -> None:
    for keyname in (k for k in dir(Qt.Key) if k.startswith("Key")):
        key = getattr(Qt.Key, keyname)
        assert isinstance(qkey2modelkey(key), (KeyCode, KeyCombo))

    assert qkey2modelkey(Qt.Key.Key_M) == KeyCode.KeyM


def test_qkeysequence2modelkeybinding() -> None:
    seq = QKeySequence(
        Qt.Modifier.SHIFT | Qt.Key.Key_M, Qt.KeyboardModifier.NoModifier | Qt.Key.Key_K
    )
    app_key = KeyBinding(parts=[KeyMod.Shift | KeyCode.KeyM, KeyCode.KeyK])
    assert qkeysequence2modelkeybinding(seq) == app_key

    seq = QKeySequence(
        Qt.Modifier.ALT | Qt.Key.Key_M, Qt.KeyboardModifier.NoModifier | Qt.Key.Key_K
    )
    app_key = KeyBinding(parts=[KeyMod.Alt | KeyCode.KeyM, KeyCode.KeyK])
    assert qkeysequence2modelkeybinding(seq) == app_key

    seq = QKeySequence(
        Qt.Modifier.META | Qt.Key.Key_M, Qt.KeyboardModifier.NoModifier | Qt.Key.Key_K
    )
    app_key = KeyBinding(parts=[KeyMod.CtrlCmd | KeyCode.KeyM, KeyCode.KeyK])
    assert qkeysequence2modelkeybinding(seq) == app_key

    seq = QKeySequence(
        Qt.Modifier.CTRL | Qt.Key.Key_M, Qt.KeyboardModifier.NoModifier | Qt.Key.Key_K
    )
    app_key = KeyBinding(parts=[KeyMod.WinCtrl | KeyCode.KeyM, KeyCode.KeyK])
    assert qkeysequence2modelkeybinding(seq) == app_key
