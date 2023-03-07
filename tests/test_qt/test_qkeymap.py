from unittest.mock import patch

from qtpy.QtCore import Qt
from qtpy.QtGui import QKeySequence

from app_model.backends.qt import (
    _qkeymap,
    qkey2modelkey,
    qkeysequence2modelkeybinding,
    qmods2modelmods,
)
from app_model.backends.qt._qkeymap import modelkey2qkey
from app_model.types import KeyBinding, KeyCode, KeyCombo, KeyMod

# stuff we don't know how to deal with yet


def test_modelkey_lookup() -> None:
    assert modelkey2qkey(KeyCode.KeyM) == Qt.Key.Key_M

    with patch.object(_qkeymap, "MAC", True):
        with patch.object(_qkeymap, "_mac_ctrl_meta_swapped", return_value=False):
            assert modelkey2qkey(KeyCode.Ctrl) == Qt.Key.Key_Control
            assert modelkey2qkey(KeyCode.Meta) == Qt.Key.Key_Meta
        with patch.object(_qkeymap, "_mac_ctrl_meta_swapped", return_value=True):
            assert modelkey2qkey(KeyCode.Meta) == Qt.Key.Key_Control
            assert modelkey2qkey(KeyCode.Ctrl) == Qt.Key.Key_Meta

    with patch.object(_qkeymap, "MAC", False):
        assert modelkey2qkey(KeyCode.Ctrl) == Qt.Key.Key_Control
        assert modelkey2qkey(KeyCode.Meta) == Qt.Key.Key_Meta


def test_qkey_lookup() -> None:
    for keyname in (k for k in dir(Qt.Key) if k.startswith("Key")):
        key = getattr(Qt.Key, keyname)
        assert isinstance(qkey2modelkey(key), (KeyCode, KeyCombo))

    assert qkey2modelkey(Qt.Key.Key_M) == KeyCode.KeyM

    with patch.object(_qkeymap, "MAC", True):
        with patch.object(_qkeymap, "_mac_ctrl_meta_swapped", return_value=False):
            assert qkey2modelkey(Qt.Key.Key_Control) == KeyCode.Ctrl
            assert qkey2modelkey(Qt.Key.Key_Meta) == KeyCode.Meta
        with patch.object(_qkeymap, "_mac_ctrl_meta_swapped", return_value=True):
            assert qkey2modelkey(Qt.Key.Key_Control) == KeyCode.Meta
            assert qkey2modelkey(Qt.Key.Key_Meta) == KeyCode.Ctrl

    with patch.object(_qkeymap, "MAC", False):
        assert qkey2modelkey(Qt.Key.Key_Control) == KeyCode.Ctrl
        assert qkey2modelkey(Qt.Key.Key_Meta) == KeyCode.Meta


def test_qmod_lookup() -> None:
    assert qmods2modelmods(Qt.KeyboardModifier.ShiftModifier) == KeyMod.Shift
    assert qmods2modelmods(Qt.KeyboardModifier.AltModifier) == KeyMod.Alt

    with patch.object(_qkeymap, "MAC", True):
        with patch.object(_qkeymap, "_mac_ctrl_meta_swapped", return_value=False):
            assert (
                qmods2modelmods(Qt.KeyboardModifier.ControlModifier) == KeyMod.WinCtrl
            )
            assert qmods2modelmods(Qt.KeyboardModifier.MetaModifier) == KeyMod.CtrlCmd

        with patch.object(_qkeymap, "_mac_ctrl_meta_swapped", return_value=True):
            assert (
                qmods2modelmods(Qt.KeyboardModifier.ControlModifier) == KeyMod.CtrlCmd
            )
            assert qmods2modelmods(Qt.KeyboardModifier.MetaModifier) == KeyMod.WinCtrl

    with patch.object(_qkeymap, "MAC", False):
        assert qmods2modelmods(Qt.KeyboardModifier.ControlModifier) == KeyMod.CtrlCmd
        assert qmods2modelmods(Qt.KeyboardModifier.MetaModifier) == KeyMod.WinCtrl


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

    with patch.object(_qkeymap, "MAC", True):
        with patch.object(_qkeymap, "_mac_ctrl_meta_swapped", return_value=False):
            # on Macs, unswapped, Meta -> Cmd
            seq = QKeySequence(
                Qt.Modifier.META | Qt.Key.Key_M,
                Qt.KeyboardModifier.NoModifier | Qt.Key.Key_K,
            )
            app_key = KeyBinding(parts=[KeyMod.CtrlCmd | KeyCode.KeyM, KeyCode.KeyK])
            assert qkeysequence2modelkeybinding(seq) == app_key

            # on Macs, unswapped, Ctrl -> Ctrl
            seq = QKeySequence(
                Qt.Modifier.CTRL | Qt.Key.Key_M,
                Qt.KeyboardModifier.NoModifier | Qt.Key.Key_K,
            )
            app_key = KeyBinding(parts=[KeyMod.WinCtrl | KeyCode.KeyM, KeyCode.KeyK])
            assert qkeysequence2modelkeybinding(seq) == app_key

            seq = QKeySequence(
                Qt.Modifier.META | Qt.Key.Key_Meta,
                Qt.Modifier.CTRL | Qt.Key.Key_Control,
            )
            app_key = KeyBinding(
                parts=[KeyMod.CtrlCmd | KeyCode.Meta, KeyMod.WinCtrl | KeyCode.Ctrl]
            )
            assert qkeysequence2modelkeybinding(seq) == app_key

        with patch.object(_qkeymap, "_mac_ctrl_meta_swapped", return_value=True):
            # on Mac swapped, Ctrl -> Meta/Cmd
            seq = QKeySequence(
                Qt.Modifier.CTRL | Qt.Key.Key_M,
                Qt.KeyboardModifier.NoModifier | Qt.Key.Key_K,
            )
            app_key = KeyBinding(parts=[KeyMod.CtrlCmd | KeyCode.KeyM, KeyCode.KeyK])
            assert qkeysequence2modelkeybinding(seq) == app_key

            # on Mac swapped, Meta/Cmd -> Ctrl
            seq = QKeySequence(
                Qt.Modifier.META | Qt.Key.Key_M,
                Qt.KeyboardModifier.NoModifier | Qt.Key.Key_K,
            )
            app_key = KeyBinding(parts=[KeyMod.WinCtrl | KeyCode.KeyM, KeyCode.KeyK])
            assert qkeysequence2modelkeybinding(seq) == app_key

            seq = QKeySequence(
                Qt.Modifier.META | Qt.Key.Key_Meta,
                Qt.Modifier.CTRL | Qt.Key.Key_Control,
            )
            app_key = KeyBinding(
                parts=[KeyMod.WinCtrl | KeyCode.Ctrl, KeyMod.CtrlCmd | KeyCode.Meta]
            )
            assert qkeysequence2modelkeybinding(seq) == app_key

    with patch.object(_qkeymap, "MAC", False):
        # on Win/Unix, Ctrl -> Ctrl
        seq = QKeySequence(
            Qt.Modifier.CTRL | Qt.Key.Key_M,
            Qt.KeyboardModifier.NoModifier | Qt.Key.Key_K,
        )
        app_key = KeyBinding(parts=[KeyMod.CtrlCmd | KeyCode.KeyM, KeyCode.KeyK])
        assert qkeysequence2modelkeybinding(seq) == app_key

        # on Win, Meta -> Win, on Unix, Meta -> Super
        seq = QKeySequence(
            Qt.Modifier.META | Qt.Key.Key_M,
            Qt.KeyboardModifier.NoModifier | Qt.Key.Key_K,
        )
        app_key = KeyBinding(parts=[KeyMod.WinCtrl | KeyCode.KeyM, KeyCode.KeyK])
        assert qkeysequence2modelkeybinding(seq) == app_key

        seq = QKeySequence(
            Qt.Modifier.META | Qt.Key.Key_Meta,
            Qt.Modifier.CTRL | Qt.Key.Key_Control,
        )
        app_key = KeyBinding(
            parts=[KeyMod.WinCtrl | KeyCode.Meta, KeyMod.CtrlCmd | KeyCode.Ctrl]
        )
        assert qkeysequence2modelkeybinding(seq) == app_key
