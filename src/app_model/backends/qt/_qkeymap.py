import operator
from functools import reduce
from typing import Dict, Optional, Union, cast

from qtpy.QtCore import Qt
from qtpy.QtGui import QKeySequence

from ...types._constants import OperatingSystem
from ...types._keys import KeyBinding, KeyCode, KeyCombo, KeyMod, SimpleKeyBinding

try:
    from qtpy import QT6
except ImportError:
    QT6 = False


QMETA = Qt.KeyboardModifier.MetaModifier
QCTRL = Qt.KeyboardModifier.ControlModifier

MAC = OperatingSystem.current().is_mac
_QMOD_LOOKUP: Dict[str, Qt.KeyboardModifier] = {
    "ctrl": QMETA if MAC else QCTRL,
    "shift": Qt.KeyboardModifier.ShiftModifier,
    "alt": Qt.KeyboardModifier.AltModifier,
    "meta": QCTRL if MAC else QMETA,
}


if QT6:
    from qtpy.QtCore import QKeyCombination

    def simple_keybinding_to_qint(skb: SimpleKeyBinding) -> int:
        """Create Qt Key integer from a SimpleKeyBinding."""
        key = KEY_TO_QT.get(skb.key, 0)
        mods = (v for k, v in _QMOD_LOOKUP.items() if getattr(skb, k))
        combo = QKeyCombination(reduce(operator.or_, mods), key)
        return cast(int, combo.toCombined())

else:
    QKeyCombination = int

    def simple_keybinding_to_qint(skb: SimpleKeyBinding) -> int:
        """Create Qt Key integer from a SimpleKeyBinding."""
        out = KEY_TO_QT.get(skb.key, 0)
        mods = (v for k, v in _QMOD_LOOKUP.items() if getattr(skb, k))
        out = reduce(operator.or_, mods, out)
        return int(out)


# maybe ~ 1.5x faster than:
# QKeySequence.fromString(",".join(str(x) for x in kb.parts))
# but the string version might be more reliable?
class QKeyBindingSequence(QKeySequence):
    """A QKeySequence based on a KeyBinding instance."""

    def __init__(self, kb: KeyBinding) -> None:
        ints = [simple_keybinding_to_qint(skb) for skb in kb.parts]
        super().__init__(*ints)


KEY_TO_QT: Dict[Optional[KeyCode], Qt.Key] = {
    None: Qt.Key.Key_unknown,
    KeyCode.UNKOWN: Qt.Key.Key_unknown,
    KeyCode.Backquote: Qt.Key.Key_QuoteLeft,
    KeyCode.Backslash: Qt.Key.Key_Backslash,
    KeyCode.IntlBackslash: Qt.Key.Key_Backslash,
    KeyCode.BracketLeft: Qt.Key.Key_BracketLeft,
    KeyCode.BracketRight: Qt.Key.Key_BracketRight,
    KeyCode.Comma: Qt.Key.Key_Comma,
    KeyCode.Digit0: Qt.Key.Key_0,
    KeyCode.Digit1: Qt.Key.Key_1,
    KeyCode.Digit2: Qt.Key.Key_2,
    KeyCode.Digit3: Qt.Key.Key_3,
    KeyCode.Digit4: Qt.Key.Key_4,
    KeyCode.Digit5: Qt.Key.Key_5,
    KeyCode.Digit6: Qt.Key.Key_6,
    KeyCode.Digit7: Qt.Key.Key_7,
    KeyCode.Digit8: Qt.Key.Key_8,
    KeyCode.Digit9: Qt.Key.Key_9,
    KeyCode.Equal: Qt.Key.Key_Equal,
    KeyCode.KeyA: Qt.Key.Key_A,
    KeyCode.KeyB: Qt.Key.Key_B,
    KeyCode.KeyC: Qt.Key.Key_C,
    KeyCode.KeyD: Qt.Key.Key_D,
    KeyCode.KeyE: Qt.Key.Key_E,
    KeyCode.KeyF: Qt.Key.Key_F,
    KeyCode.KeyG: Qt.Key.Key_G,
    KeyCode.KeyH: Qt.Key.Key_H,
    KeyCode.KeyI: Qt.Key.Key_I,
    KeyCode.KeyJ: Qt.Key.Key_J,
    KeyCode.KeyK: Qt.Key.Key_K,
    KeyCode.KeyL: Qt.Key.Key_L,
    KeyCode.KeyM: Qt.Key.Key_M,
    KeyCode.KeyN: Qt.Key.Key_N,
    KeyCode.KeyO: Qt.Key.Key_O,
    KeyCode.KeyP: Qt.Key.Key_P,
    KeyCode.KeyQ: Qt.Key.Key_Q,
    KeyCode.KeyR: Qt.Key.Key_R,
    KeyCode.KeyS: Qt.Key.Key_S,
    KeyCode.KeyT: Qt.Key.Key_T,
    KeyCode.KeyU: Qt.Key.Key_U,
    KeyCode.KeyV: Qt.Key.Key_V,
    KeyCode.KeyW: Qt.Key.Key_W,
    KeyCode.KeyX: Qt.Key.Key_X,
    KeyCode.KeyY: Qt.Key.Key_Y,
    KeyCode.KeyZ: Qt.Key.Key_Z,
    KeyCode.Minus: Qt.Key.Key_Minus,
    KeyCode.Period: Qt.Key.Key_Period,
    KeyCode.Quote: Qt.Key.Key_Apostrophe,
    KeyCode.Semicolon: Qt.Key.Key_Semicolon,
    KeyCode.Slash: Qt.Key.Key_Slash,
    KeyCode.Alt: Qt.Key.Key_Alt,
    KeyCode.Backspace: Qt.Key.Key_Backspace,
    KeyCode.CapsLock: Qt.Key.Key_CapsLock,
    KeyCode.ContextMenu: Qt.Key.Key_Context1,
    KeyCode.Ctrl: Qt.Key.Key_Control,
    KeyCode.Enter: Qt.Key.Key_Enter,
    KeyCode.Meta: Qt.Key.Key_Meta,
    KeyCode.Shift: Qt.Key.Key_Shift,
    KeyCode.Space: Qt.Key.Key_Space,
    KeyCode.Tab: Qt.Key.Key_Tab,
    KeyCode.Delete: Qt.Key.Key_Delete,
    KeyCode.End: Qt.Key.Key_End,
    KeyCode.Home: Qt.Key.Key_Home,
    KeyCode.Insert: Qt.Key.Key_Insert,
    KeyCode.PageDown: Qt.Key.Key_PageDown,
    KeyCode.PageUp: Qt.Key.Key_PageUp,
    KeyCode.DownArrow: Qt.Key.Key_Down,
    KeyCode.LeftArrow: Qt.Key.Key_Left,
    KeyCode.RightArrow: Qt.Key.Key_Right,
    KeyCode.UpArrow: Qt.Key.Key_Up,
    KeyCode.NumLock: Qt.Key.Key_NumLock,
    KeyCode.Numpad0: Qt.KeyboardModifier.KeypadModifier | Qt.Key.Key_0,
    KeyCode.Numpad1: Qt.KeyboardModifier.KeypadModifier | Qt.Key.Key_1,
    KeyCode.Numpad2: Qt.KeyboardModifier.KeypadModifier | Qt.Key.Key_2,
    KeyCode.Numpad3: Qt.KeyboardModifier.KeypadModifier | Qt.Key.Key_3,
    KeyCode.Numpad4: Qt.KeyboardModifier.KeypadModifier | Qt.Key.Key_4,
    KeyCode.Numpad5: Qt.KeyboardModifier.KeypadModifier | Qt.Key.Key_5,
    KeyCode.Numpad6: Qt.KeyboardModifier.KeypadModifier | Qt.Key.Key_6,
    KeyCode.Numpad7: Qt.KeyboardModifier.KeypadModifier | Qt.Key.Key_7,
    KeyCode.Numpad8: Qt.KeyboardModifier.KeypadModifier | Qt.Key.Key_8,
    KeyCode.Numpad9: Qt.KeyboardModifier.KeypadModifier | Qt.Key.Key_9,
    KeyCode.NumpadAdd: Qt.KeyboardModifier.KeypadModifier | Qt.Key.Key_Plus,
    KeyCode.NumpadDecimal: Qt.KeyboardModifier.KeypadModifier | Qt.Key.Key_Period,
    KeyCode.NumpadDivide: Qt.KeyboardModifier.KeypadModifier | Qt.Key.Key_Slash,
    KeyCode.NumpadMultiply: Qt.KeyboardModifier.KeypadModifier | Qt.Key.Key_Asterisk,
    KeyCode.NumpadSubtract: Qt.KeyboardModifier.KeypadModifier | Qt.Key.Key_Minus,
    KeyCode.Escape: Qt.Key.Key_Escape,
    KeyCode.F1: Qt.Key.Key_F1,
    KeyCode.F2: Qt.Key.Key_F2,
    KeyCode.F3: Qt.Key.Key_F3,
    KeyCode.F4: Qt.Key.Key_F4,
    KeyCode.F5: Qt.Key.Key_F5,
    KeyCode.F6: Qt.Key.Key_F6,
    KeyCode.F7: Qt.Key.Key_F7,
    KeyCode.F8: Qt.Key.Key_F8,
    KeyCode.F9: Qt.Key.Key_F9,
    KeyCode.F10: Qt.Key.Key_F10,
    KeyCode.F11: Qt.Key.Key_F11,
    KeyCode.F12: Qt.Key.Key_F12,
    KeyCode.ScrollLock: Qt.Key.Key_ScrollLock,
    KeyCode.PauseBreak: Qt.Key.Key_Pause,
}

KEYMOD_TO_QT = {
    KeyMod.NONE: Qt.KeyboardModifier.NoModifier,
    KeyMod.Alt: Qt.KeyboardModifier.AltModifier,
    KeyMod.CtrlCmd: Qt.KeyboardModifier.ControlModifier,
    KeyMod.Shift: Qt.KeyboardModifier.ShiftModifier,
    KeyMod.WinCtrl: Qt.KeyboardModifier.MetaModifier,
}


# unused/untested
KEY_FROM_QT: Dict[Qt.Key, KeyCode] = {
    v.toCombined() if hasattr(v, "toCombined") else int(v): k
    for k, v in KEY_TO_QT.items()
    if k
}

# Qt Keys which have no representation in the W3C spec
_QTONLY_KEYS = {
    Qt.Key.Key_Exclam: KeyMod.Shift | KeyCode.Digit1,
    Qt.Key.Key_At: KeyMod.Shift | KeyCode.Digit2,
    Qt.Key.Key_NumberSign: KeyMod.Shift | KeyCode.Digit3,
    Qt.Key.Key_Dollar: KeyMod.Shift | KeyCode.Digit4,
    Qt.Key.Key_Percent: KeyMod.Shift | KeyCode.Digit5,
    Qt.Key.Key_AsciiCircum: KeyMod.Shift | KeyCode.Digit6,
    Qt.Key.Key_Ampersand: KeyMod.Shift | KeyCode.Digit7,
    Qt.Key.Key_Asterisk: KeyMod.Shift | KeyCode.Digit8,
    Qt.Key.Key_ParenLeft: KeyMod.Shift | KeyCode.Digit9,
    Qt.Key.Key_ParenRight: KeyMod.Shift | KeyCode.Digit0,
    Qt.Key.Key_Underscore: KeyMod.Shift | KeyCode.Minus,
    Qt.Key.Key_Plus: KeyMod.Shift | KeyCode.Equal,
    Qt.Key.Key_BraceLeft: KeyMod.Shift | KeyCode.BracketLeft,
    Qt.Key.Key_BraceRight: KeyMod.Shift | KeyCode.BracketRight,
    Qt.Key.Key_Bar: KeyMod.Shift | KeyCode.Backslash,
    Qt.Key.Key_Colon: KeyMod.Shift | KeyCode.Semicolon,
    Qt.Key.Key_QuoteDbl: KeyMod.Shift | KeyCode.Quote,
    Qt.Key.Key_Less: KeyMod.Shift | KeyCode.Comma,
    Qt.Key.Key_Greater: KeyMod.Shift | KeyCode.Period,
    Qt.Key.Key_Question: KeyMod.Shift | KeyCode.Slash,
    Qt.Key.Key_AsciiTilde: KeyMod.Shift | KeyCode.Backquote,
    Qt.Key.Key_Return: KeyCode.Enter,
}
KEY_FROM_QT.update(_QTONLY_KEYS)


def qmods2modelmods(modifiers: Qt.KeyboardModifier) -> KeyMod:
    """Return KeyMod from Qt.KeyboardModifier."""
    mod = KeyMod.NONE
    if modifiers & Qt.KeyboardModifier.ShiftModifier:
        mod |= KeyMod.Shift
    if modifiers & Qt.KeyboardModifier.ControlModifier:
        mod |= KeyMod.WinCtrl
    if modifiers & Qt.KeyboardModifier.AltModifier:
        mod |= KeyMod.Alt
    if modifiers & Qt.KeyboardModifier.MetaModifier:
        mod |= KeyMod.CtrlCmd
    return mod


def qkey2modelkey(key: Qt.Key) -> KeyCode:
    """Return KeyCode from Qt.Key."""
    return KEY_FROM_QT.get(key, KeyCode.UNKOWN)


def qkeycombo2modelkey(key: QKeyCombination) -> Union[KeyCode, KeyCombo]:
    """Return KeyCode or KeyCombo from QKeyCombination."""
    if key in KEY_FROM_QT:
        return KEY_FROM_QT[key]
    qmods = Qt.KeyboardModifier(key & Qt.KeyboardModifier.KeyboardModifierMask)
    qkey = Qt.Key(key & ~Qt.KeyboardModifier.KeyboardModifierMask)
    return cast(KeyCombo, qmods2modelmods(qmods) | qkey2modelkey(qkey))


def qkeysequence2modelkeybinding(key: QKeySequence) -> KeyBinding:
    """Return KeyBinding from QKeySequence."""
    # FIXME: this should return KeyChord instead of KeyBinding... but that only takes 2
    return KeyBinding(parts=[qkeycombo2modelkey(x) for x in key])
