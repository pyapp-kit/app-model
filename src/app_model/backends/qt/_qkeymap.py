# mypy: disable-error-code="operator"
from __future__ import annotations

import operator
from functools import reduce
from typing import TYPE_CHECKING, Mapping, MutableMapping

from qtpy import API, QT_VERSION
from qtpy.QtCore import QCoreApplication, Qt
from qtpy.QtGui import QKeySequence

from app_model.types import (
    KeyBinding,
    KeyCode,
    KeyCombo,
    KeyMod,
    SimpleKeyBinding,
)
from app_model.types._constants import OperatingSystem

if TYPE_CHECKING:
    from qtpy.QtCore import QKeyCombination

try:
    from qtpy import QT6
except ImportError:
    QT6 = False

QCTRL = Qt.KeyboardModifier.ControlModifier
QSHIFT = Qt.KeyboardModifier.ShiftModifier
QALT = Qt.KeyboardModifier.AltModifier
QMETA = Qt.KeyboardModifier.MetaModifier

MAC = OperatingSystem.current().is_mac

_QMOD_LOOKUP = {
    "ctrl": QCTRL,
    "shift": QSHIFT,
    "alt": QALT,
    "meta": QMETA,
}

_SWAPPED_QMOD_LOOKUP = {
    **_QMOD_LOOKUP,
    "ctrl": QMETA,
    "meta": QCTRL,
}


def _mac_ctrl_meta_swapped() -> bool:
    """Return True if Qt is swapping Ctrl and Meta for keyboard interactions."""
    return not QCoreApplication.testAttribute(
        Qt.ApplicationAttribute.AA_MacDontSwapCtrlAndMeta
    )


if QT6:
    from qtpy.QtCore import QKeyCombination

    def simple_keybinding_to_qint(skb: SimpleKeyBinding) -> int:
        """Create Qt Key integer from a SimpleKeyBinding."""
        lookup = (
            _SWAPPED_QMOD_LOOKUP if MAC and _mac_ctrl_meta_swapped() else _QMOD_LOOKUP
        )
        key = modelkey2qkey(skb.key) if skb.key else Qt.Key.Key_unknown
        mods = (v for k, v in lookup.items() if getattr(skb, k))
        combo = QKeyCombination(
            reduce(operator.or_, mods, Qt.KeyboardModifier.NoModifier), key
        )
        return int(combo.toCombined())

else:

    def simple_keybinding_to_qint(skb: SimpleKeyBinding) -> int:
        """Create Qt Key integer from a SimpleKeyBinding."""
        lookup = (
            _SWAPPED_QMOD_LOOKUP if MAC and _mac_ctrl_meta_swapped() else _QMOD_LOOKUP
        )
        out = modelkey2qkey(skb.key) if skb.key else 0
        mods = (v for k, v in lookup.items() if getattr(skb, k))
        out = reduce(operator.or_, mods, out)
        return int(out)


if QT6 and not (API == "pyside6" and int(QT_VERSION[2]) < 4):

    def _get_qmods(key: QKeyCombination) -> Qt.KeyboardModifier:
        return key.keyboardModifiers()

    def _get_qkey(key: QKeyCombination) -> Qt.Key:
        return key.key()

else:

    def _get_qmods(key: QKeyCombination) -> Qt.KeyboardModifier:
        return Qt.KeyboardModifier(key & Qt.KeyboardModifier.KeyboardModifierMask)

    def _get_qkey(key: QKeyCombination) -> Qt.Key:
        return Qt.Key(key & ~Qt.KeyboardModifier.KeyboardModifierMask)


# maybe ~ 1.5x faster than:
# QKeySequence.fromString(",".join(str(x) for x in kb.parts))
# but the string version might be more reliable?
class QKeyBindingSequence(QKeySequence):
    """A QKeySequence based on a KeyBinding instance."""

    def __init__(self, kb: KeyBinding) -> None:
        ints = [simple_keybinding_to_qint(skb) for skb in kb.parts]
        super().__init__(*ints)


KEY_TO_QT: dict[KeyCode | None, Qt.Key] = {
    None: Qt.Key.Key_unknown,
    KeyCode.UNKNOWN: Qt.Key.Key_unknown,
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
    KeyCode.PrintScreen: Qt.Key.Key_Print,
    KeyCode.ScrollLock: Qt.Key.Key_ScrollLock,
    KeyCode.PauseBreak: Qt.Key.Key_Pause,
}

KEYMOD_FROM_QT = {
    Qt.KeyboardModifier.NoModifier: KeyMod.NONE,
    QALT: KeyMod.Alt,
    QCTRL: KeyMod.CtrlCmd,
    QSHIFT: KeyMod.Shift,
    QMETA: KeyMod.WinCtrl,
}

MAC_KEYMOD_FROM_QT = {**KEYMOD_FROM_QT, QCTRL: KeyMod.WinCtrl, QMETA: KeyMod.CtrlCmd}

KEYMOD_TO_QT = {
    KeyMod.NONE: Qt.KeyboardModifier.NoModifier,
    KeyMod.CtrlCmd: QCTRL,
    KeyMod.Alt: QALT,
    KeyMod.Shift: QSHIFT,
    KeyMod.WinCtrl: QMETA,
}

MAC_KEYMOD_TO_QT = {**KEYMOD_TO_QT, KeyMod.WinCtrl: QCTRL, KeyMod.CtrlCmd: QMETA}


KEY_FROM_QT: MutableMapping[Qt.Key, KeyCode | KeyCombo] = {
    v.toCombined() if hasattr(v, "toCombined") else int(v): k
    for k, v in KEY_TO_QT.items()
    if k
}

# Qt Keys which have no representation in the W3C spec
_QTONLY_KEYS: Mapping[Qt.Key, KeyCode | KeyCombo] = {
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
    Qt.Key.Key_Backtab: KeyMod.Shift | KeyCode.Tab,
}
KEY_FROM_QT.update(_QTONLY_KEYS)


def qmods2modelmods(modifiers: Qt.KeyboardModifier) -> KeyMod:
    """Return KeyMod from Qt.KeyboardModifier."""
    mod = KeyMod.NONE
    lookup = (
        MAC_KEYMOD_FROM_QT if MAC and not _mac_ctrl_meta_swapped() else KEYMOD_FROM_QT
    )
    for modifier in lookup:
        if modifiers & modifier:
            mod |= lookup[modifier]
    return mod


def modelkey2qkey(key: KeyCode) -> Qt.Key:
    """Return Qt.Key from KeyCode."""
    if MAC and _mac_ctrl_meta_swapped():
        if key == KeyCode.Meta:
            return Qt.Key.Key_Control
        if key == KeyCode.Ctrl:
            return Qt.Key.Key_Meta
    return KEY_TO_QT.get(key, Qt.Key.Key_unknown)


def qkey2modelkey(key: Qt.Key) -> KeyCode | KeyCombo:
    """Return KeyCode from Qt.Key."""
    if MAC and _mac_ctrl_meta_swapped():
        if key == Qt.Key.Key_Control:
            return KeyCode.Meta
        if key == Qt.Key.Key_Meta:
            return KeyCode.Ctrl
    return KEY_FROM_QT.get(key, KeyCode.UNKNOWN)


def qkeycombo2modelkey(key: QKeyCombination) -> KeyCode | KeyCombo:
    """Return KeyCode or KeyCombo from QKeyCombination."""
    if key in KEY_FROM_QT:
        # type ignore because in qt5, key may actually just be int ... but it's fine.
        return KEY_FROM_QT[key]
    qmods = _get_qmods(key)
    qkey = _get_qkey(key)
    return qmods2modelmods(qmods) | qkey2modelkey(qkey)  # type: ignore [return-value]


def qkeysequence2modelkeybinding(key: QKeySequence) -> KeyBinding:
    """Return KeyBinding from QKeySequence."""
    # FIXME: this should return KeyChord instead of KeyBinding... but that only takes 2
    parts = [SimpleKeyBinding.from_int(qkeycombo2modelkey(x)) for x in iter(key)]
    return KeyBinding(parts=parts)


# ################# These are the Qkeys we currently aren't mapping ################ #
# Key_F14
# Key_F15
# Key_F16
# Key_F17
# Key_F18
# Key_F19
# Key_F20
# Key_F21
# Key_F22
# Key_F23
# Key_F24
# Key_F25
# Key_F26
# Key_F27
# Key_F28
# Key_F29
# Key_F30
# Key_F31
# Key_F32
# Key_F33
# Key_F34
# Key_F35
# Key_Super_L
# Key_Super_R
# Key_Menu
# Key_Hyper_L
# Key_Hyper_R
# Key_Help
# Key_Direction_L
# Key_Direction_R
# Key_nobreakspace
# Key_exclamdown
# Key_cent
# Key_sterling
# Key_currency
# Key_yen
# Key_brokenbar
# Key_section
# Key_diaeresis
# Key_copyright
# Key_ordfeminine
# Key_guillemotleft
# Key_notsign
# Key_hyphen
# Key_registered
# Key_macron
# Key_degree
# Key_plusminus
# Key_twosuperior
# Key_threesuperior
# Key_acute
# Key_mu
# Key_paragraph
# Key_periodcentered
# Key_cedilla
# Key_onesuperior
# Key_masculine
# Key_guillemotright
# Key_onequarter
# Key_onehalf
# Key_threequarters
# Key_questiondown
# Key_Agrave
# Key_Aacute
# Key_Acircumflex
# Key_Atilde
# Key_Adiaeresis
# Key_Aring
# Key_AE
# Key_Ccedilla
# Key_Egrave
# Key_Eacute
# Key_Ecircumflex
# Key_Ediaeresis
# Key_Igrave
# Key_Iacute
# Key_Icircumflex
# Key_Idiaeresis
# Key_ETH
# Key_Ntilde
# Key_Ograve
# Key_Oacute
# Key_Ocircumflex
# Key_Otilde
# Key_Odiaeresis
# Key_multiply
# Key_Ooblique
# Key_Ugrave
# Key_Uacute
# Key_Ucircumflex
# Key_Udiaeresis
# Key_Yacute
# Key_THORN
# Key_ssharp
# Key_division
# Key_ydiaeresis
# Key_AltGr
# Key_Multi_key
# Key_Codeinput
# Key_SingleCandidate
# Key_MultipleCandidate
# Key_PreviousCandidate
# Key_Mode_switch
# Key_Kanji
# Key_Muhenkan
# Key_Henkan
# Key_Romaji
# Key_Hiragana
# Key_Katakana
# Key_Hiragana_Katakana
# Key_Zenkaku
# Key_Hankaku
# Key_Zenkaku_Hankaku
# Key_Touroku
# Key_Massyo
# Key_Kana_Lock
# Key_Kana_Shift
# Key_Eisu_Shift
# Key_Eisu_toggle
# Key_Hangul
# Key_Hangul_Start
# Key_Hangul_End
# Key_Hangul_Hanja
# Key_Hangul_Jamo
# Key_Hangul_Romaja
# Key_Hangul_Jeonja
# Key_Hangul_Banja
# Key_Hangul_PreHanja
# Key_Hangul_PostHanja
# Key_Hangul_Special
# Key_Dead_Grave
# Key_Dead_Acute
# Key_Dead_Circumflex
# Key_Dead_Tilde
# Key_Dead_Macron
# Key_Dead_Breve
# Key_Dead_Abovedot
# Key_Dead_Diaeresis
# Key_Dead_Abovering
# Key_Dead_Doubleacute
# Key_Dead_Caron
# Key_Dead_Cedilla
# Key_Dead_Ogonek
# Key_Dead_Iota
# Key_Dead_Voiced_Sound
# Key_Dead_Semivoiced_Sound
# Key_Dead_Belowdot
# Key_Dead_Hook
# Key_Dead_Horn
# Key_Dead_Stroke
# Key_Dead_Abovecomma
# Key_Dead_Abovereversedcomma
# Key_Dead_Doublegrave
# Key_Dead_Belowring
# Key_Dead_Belowmacron
# Key_Dead_Belowcircumflex
# Key_Dead_Belowtilde
# Key_Dead_Belowbreve
# Key_Dead_Belowdiaeresis
# Key_Dead_Invertedbreve
# Key_Dead_Belowcomma
# Key_Dead_Currency
# Key_Dead_a
# Key_Dead_A
# Key_Dead_e
# Key_Dead_E
# Key_Dead_i
# Key_Dead_I
# Key_Dead_o
# Key_Dead_O
# Key_Dead_u
# Key_Dead_U
# Key_Dead_Small_Schwa
# Key_Dead_Capital_Schwa
# Key_Dead_Greek
# Key_Dead_Lowline
# Key_Dead_Aboveverticalline
# Key_Dead_Belowverticalline
# Key_Dead_Longsolidusoverlay
# Key_Back
# Key_Forward
# Key_Stop
# Key_Refresh
# Key_VolumeDown
# Key_VolumeMute
# Key_VolumeUp
# Key_BassBoost
# Key_BassUp
# Key_BassDown
# Key_TrebleUp
# Key_TrebleDown
# Key_MediaPlay
# Key_MediaStop
# Key_MediaPrevious
# Key_MediaNext
# Key_MediaRecord
# Key_MediaPause
# Key_MediaTogglePlayPause
# Key_HomePage
# Key_Favorites
# Key_Search
# Key_Standby
# Key_OpenUrl
# Key_LaunchMail
# Key_LaunchMedia
# Key_Launch0
# Key_Launch1
# Key_Launch2
# Key_Launch3
# Key_Launch4
# Key_Launch5
# Key_Launch6
# Key_Launch7
# Key_Launch8
# Key_Launch9
# Key_LaunchA
# Key_LaunchB
# Key_LaunchC
# Key_LaunchD
# Key_LaunchE
# Key_LaunchF
# Key_MonBrightnessUp
# Key_MonBrightnessDown
# Key_KeyboardLightOnOff
# Key_KeyboardBrightnessUp
# Key_KeyboardBrightnessDown
# Key_PowerOff
# Key_WakeUp
# Key_Eject
# Key_ScreenSaver
# Key_WWW
# Key_Memo
# Key_LightBulb
# Key_Shop
# Key_History
# Key_AddFavorite
# Key_HotLinks
# Key_BrightnessAdjust
# Key_Finance
# Key_Community
# Key_AudioRewind
# Key_BackForward
# Key_ApplicationLeft
# Key_ApplicationRight
# Key_Book
# Key_CD
# Key_Calculator
# Key_ToDoList
# Key_ClearGrab
# Key_Close
# Key_Copy
# Key_Cut
# Key_Display
# Key_DOS
# Key_Documents
# Key_Excel
# Key_Explorer
# Key_Game
# Key_Go
# Key_iTouch
# Key_LogOff
# Key_Market
# Key_Meeting
# Key_MenuKB
# Key_MenuPB
# Key_MySites
# Key_News
# Key_OfficeHome
# Key_Option
# Key_Paste
# Key_Phone
# Key_Calendar
# Key_Reply
# Key_Reload
# Key_RotateWindows
# Key_RotationPB
# Key_RotationKB
# Key_Save
# Key_Send
# Key_Spell
# Key_SplitScreen
# Key_Support
# Key_TaskPane
# Key_Terminal
# Key_Tools
# Key_Travel
# Key_Video
# Key_Word
# Key_Xfer
# Key_ZoomIn
# Key_ZoomOut
# Key_Away
# Key_Messenger
# Key_WebCam
# Key_MailForward
# Key_Pictures
# Key_Music
# Key_Battery
# Key_Bluetooth
# Key_WLAN
# Key_UWB
# Key_AudioForward
# Key_AudioRepeat
# Key_AudioRandomPlay
# Key_Subtitle
# Key_AudioCycleTrack
# Key_Time
# Key_Hibernate
# Key_View
# Key_TopMenu
# Key_PowerDown
# Key_Suspend
# Key_ContrastAdjust
# Key_LaunchG
# Key_LaunchH
# Key_TouchpadToggle
# Key_TouchpadOn
# Key_TouchpadOff
# Key_MicMute
# Key_Red
# Key_Green
# Key_Yellow
# Key_Blue
# Key_ChannelUp
# Key_ChannelDown
# Key_Guide
# Key_Info
# Key_Settings
# Key_MicVolumeUp
# Key_MicVolumeDown
# Key_New
# Key_Open
# Key_Find
# Key_Undo
# Key_Redo
# Key_MediaLast
# Key_Select
# Key_Yes
# Key_No
# Key_Cancel
# Key_Printer
# Key_Execute
# Key_Sleep
# Key_Play
# Key_Zoom
# Key_Exit
# Key_Context2
# Key_Context3
# Key_Context4
# Key_Call
# Key_Hangup
# Key_Flip
# Key_ToggleCallHangup
# Key_VoiceDial
# Key_LastNumberRedial
# Key_Camera
# Key_CameraFocus
