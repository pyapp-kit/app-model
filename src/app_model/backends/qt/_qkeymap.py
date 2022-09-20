import operator
from functools import reduce
from typing import Dict, Optional, Union, cast

from qtpy.QtCore import QCoreApplication, Qt
from qtpy.QtGui import QKeySequence

from ...types._constants import OperatingSystem
from ...types._keys import KeyBinding, KeyCode, KeyCombo, KeyMod, SimpleKeyBinding

try:
    from qtpy import PYQT6, QT6
except ImportError:
    QT6 = False
    PYQT6 = False


QMETA = Qt.KeyboardModifier.MetaModifier
QCTRL = Qt.KeyboardModifier.ControlModifier


def mac_ctrl_meta_swapped() -> bool:
    """Whether or not Qt has swapped ctrl and meta for Macs."""
    if not OperatingSystem.current().is_mac:
        return False

    app = QCoreApplication.instance()
    if app is None:
        return False

    return not app.testAttribute(Qt.AA_MacDontSwapCtrlAndMeta)


def _get_qmod_lookup() -> Dict[str, Qt.KeyboardModifier]:
    return {
        "ctrl": QMETA if mac_ctrl_meta_swapped() else QCTRL,
        "shift": Qt.KeyboardModifier.ShiftModifier,
        "alt": Qt.KeyboardModifier.AltModifier,
        "meta": QCTRL if mac_ctrl_meta_swapped() else QMETA,
    }


if QT6:
    from qtpy.QtCore import QKeyCombination

    def simple_keybinding_to_qint(skb: SimpleKeyBinding) -> int:
        """Create Qt Key integer from a SimpleKeyBinding."""
        key = KEY_TO_QT.get(skb.key, 0)
        mods = (v for k, v in _get_qmod_lookup().items() if getattr(skb, k))
        combo = QKeyCombination(reduce(operator.or_, mods), key)
        return cast(int, combo.toCombined())

else:
    QKeyCombination = int

    def simple_keybinding_to_qint(skb: SimpleKeyBinding) -> int:
        """Create Qt Key integer from a SimpleKeyBinding."""
        out = KEY_TO_QT.get(skb.key, 0)
        mods = (v for k, v in _get_qmod_lookup().items() if getattr(skb, k))
        out = reduce(operator.or_, mods, out)
        return int(out)


if PYQT6:

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


qt_keys = Qt.Key if PYQT6 else Qt

KEY_TO_QT: Dict[Optional[KeyCode], Qt.Key] = {
    None: qt_keys.Key_unknown,
    KeyCode.UNKOWN: qt_keys.Key_unknown,
    KeyCode.Backquote: qt_keys.Key_QuoteLeft,
    KeyCode.Backslash: qt_keys.Key_Backslash,
    KeyCode.IntlBackslash: qt_keys.Key_Backslash,
    KeyCode.BracketLeft: qt_keys.Key_BracketLeft,
    KeyCode.BracketRight: qt_keys.Key_BracketRight,
    KeyCode.Comma: qt_keys.Key_Comma,
    KeyCode.Digit0: qt_keys.Key_0,
    KeyCode.Digit1: qt_keys.Key_1,
    KeyCode.Digit2: qt_keys.Key_2,
    KeyCode.Digit3: qt_keys.Key_3,
    KeyCode.Digit4: qt_keys.Key_4,
    KeyCode.Digit5: qt_keys.Key_5,
    KeyCode.Digit6: qt_keys.Key_6,
    KeyCode.Digit7: qt_keys.Key_7,
    KeyCode.Digit8: qt_keys.Key_8,
    KeyCode.Digit9: qt_keys.Key_9,
    KeyCode.Equal: qt_keys.Key_Equal,
    KeyCode.KeyA: qt_keys.Key_A,
    KeyCode.KeyB: qt_keys.Key_B,
    KeyCode.KeyC: qt_keys.Key_C,
    KeyCode.KeyD: qt_keys.Key_D,
    KeyCode.KeyE: qt_keys.Key_E,
    KeyCode.KeyF: qt_keys.Key_F,
    KeyCode.KeyG: qt_keys.Key_G,
    KeyCode.KeyH: qt_keys.Key_H,
    KeyCode.KeyI: qt_keys.Key_I,
    KeyCode.KeyJ: qt_keys.Key_J,
    KeyCode.KeyK: qt_keys.Key_K,
    KeyCode.KeyL: qt_keys.Key_L,
    KeyCode.KeyM: qt_keys.Key_M,
    KeyCode.KeyN: qt_keys.Key_N,
    KeyCode.KeyO: qt_keys.Key_O,
    KeyCode.KeyP: qt_keys.Key_P,
    KeyCode.KeyQ: qt_keys.Key_Q,
    KeyCode.KeyR: qt_keys.Key_R,
    KeyCode.KeyS: qt_keys.Key_S,
    KeyCode.KeyT: qt_keys.Key_T,
    KeyCode.KeyU: qt_keys.Key_U,
    KeyCode.KeyV: qt_keys.Key_V,
    KeyCode.KeyW: qt_keys.Key_W,
    KeyCode.KeyX: qt_keys.Key_X,
    KeyCode.KeyY: qt_keys.Key_Y,
    KeyCode.KeyZ: qt_keys.Key_Z,
    KeyCode.Minus: qt_keys.Key_Minus,
    KeyCode.Period: qt_keys.Key_Period,
    KeyCode.Quote: qt_keys.Key_Apostrophe,
    KeyCode.Semicolon: qt_keys.Key_Semicolon,
    KeyCode.Slash: qt_keys.Key_Slash,
    KeyCode.Alt: qt_keys.Key_Alt,
    KeyCode.Backspace: qt_keys.Key_Backspace,
    KeyCode.CapsLock: qt_keys.Key_CapsLock,
    KeyCode.ContextMenu: qt_keys.Key_Context1,
    KeyCode.Ctrl: qt_keys.Key_Control,
    KeyCode.Enter: qt_keys.Key_Enter,
    KeyCode.Meta: qt_keys.Key_Meta,
    KeyCode.Shift: qt_keys.Key_Shift,
    KeyCode.Space: qt_keys.Key_Space,
    KeyCode.Tab: qt_keys.Key_Tab,
    KeyCode.Delete: qt_keys.Key_Delete,
    KeyCode.End: qt_keys.Key_End,
    KeyCode.Home: qt_keys.Key_Home,
    KeyCode.Insert: qt_keys.Key_Insert,
    KeyCode.PageDown: qt_keys.Key_PageDown,
    KeyCode.PageUp: qt_keys.Key_PageUp,
    KeyCode.DownArrow: qt_keys.Key_Down,
    KeyCode.LeftArrow: qt_keys.Key_Left,
    KeyCode.RightArrow: qt_keys.Key_Right,
    KeyCode.UpArrow: qt_keys.Key_Up,
    KeyCode.NumLock: qt_keys.Key_NumLock,
    KeyCode.Numpad0: Qt.KeyboardModifier.KeypadModifier | qt_keys.Key_0,
    KeyCode.Numpad1: Qt.KeyboardModifier.KeypadModifier | qt_keys.Key_1,
    KeyCode.Numpad2: Qt.KeyboardModifier.KeypadModifier | qt_keys.Key_2,
    KeyCode.Numpad3: Qt.KeyboardModifier.KeypadModifier | qt_keys.Key_3,
    KeyCode.Numpad4: Qt.KeyboardModifier.KeypadModifier | qt_keys.Key_4,
    KeyCode.Numpad5: Qt.KeyboardModifier.KeypadModifier | qt_keys.Key_5,
    KeyCode.Numpad6: Qt.KeyboardModifier.KeypadModifier | qt_keys.Key_6,
    KeyCode.Numpad7: Qt.KeyboardModifier.KeypadModifier | qt_keys.Key_7,
    KeyCode.Numpad8: Qt.KeyboardModifier.KeypadModifier | qt_keys.Key_8,
    KeyCode.Numpad9: Qt.KeyboardModifier.KeypadModifier | qt_keys.Key_9,
    KeyCode.NumpadAdd: Qt.KeyboardModifier.KeypadModifier | qt_keys.Key_Plus,
    KeyCode.NumpadDecimal: Qt.KeyboardModifier.KeypadModifier | qt_keys.Key_Period,
    KeyCode.NumpadDivide: Qt.KeyboardModifier.KeypadModifier | qt_keys.Key_Slash,
    KeyCode.NumpadMultiply: Qt.KeyboardModifier.KeypadModifier | qt_keys.Key_Asterisk,
    KeyCode.NumpadSubtract: Qt.KeyboardModifier.KeypadModifier | qt_keys.Key_Minus,
    KeyCode.Escape: qt_keys.Key_Escape,
    KeyCode.F1: qt_keys.Key_F1,
    KeyCode.F2: qt_keys.Key_F2,
    KeyCode.F3: qt_keys.Key_F3,
    KeyCode.F4: qt_keys.Key_F4,
    KeyCode.F5: qt_keys.Key_F5,
    KeyCode.F6: qt_keys.Key_F6,
    KeyCode.F7: qt_keys.Key_F7,
    KeyCode.F8: qt_keys.Key_F8,
    KeyCode.F9: qt_keys.Key_F9,
    KeyCode.F10: qt_keys.Key_F10,
    KeyCode.F11: qt_keys.Key_F11,
    KeyCode.F12: qt_keys.Key_F12,
    KeyCode.PrintScreen: qt_keys.Key_Print,
    KeyCode.ScrollLock: qt_keys.Key_ScrollLock,
    KeyCode.PauseBreak: qt_keys.Key_Pause,
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
    qt_keys.Key_Exclam: KeyMod.Shift | KeyCode.Digit1,
    qt_keys.Key_At: KeyMod.Shift | KeyCode.Digit2,
    qt_keys.Key_NumberSign: KeyMod.Shift | KeyCode.Digit3,
    qt_keys.Key_Dollar: KeyMod.Shift | KeyCode.Digit4,
    qt_keys.Key_Percent: KeyMod.Shift | KeyCode.Digit5,
    qt_keys.Key_AsciiCircum: KeyMod.Shift | KeyCode.Digit6,
    qt_keys.Key_Ampersand: KeyMod.Shift | KeyCode.Digit7,
    qt_keys.Key_Asterisk: KeyMod.Shift | KeyCode.Digit8,
    qt_keys.Key_ParenLeft: KeyMod.Shift | KeyCode.Digit9,
    qt_keys.Key_ParenRight: KeyMod.Shift | KeyCode.Digit0,
    qt_keys.Key_Underscore: KeyMod.Shift | KeyCode.Minus,
    qt_keys.Key_Plus: KeyMod.Shift | KeyCode.Equal,
    qt_keys.Key_BraceLeft: KeyMod.Shift | KeyCode.BracketLeft,
    qt_keys.Key_BraceRight: KeyMod.Shift | KeyCode.BracketRight,
    qt_keys.Key_Bar: KeyMod.Shift | KeyCode.Backslash,
    qt_keys.Key_Colon: KeyMod.Shift | KeyCode.Semicolon,
    qt_keys.Key_QuoteDbl: KeyMod.Shift | KeyCode.Quote,
    qt_keys.Key_Less: KeyMod.Shift | KeyCode.Comma,
    qt_keys.Key_Greater: KeyMod.Shift | KeyCode.Period,
    qt_keys.Key_Question: KeyMod.Shift | KeyCode.Slash,
    qt_keys.Key_AsciiTilde: KeyMod.Shift | KeyCode.Backquote,
    qt_keys.Key_Return: KeyCode.Enter,
    qt_keys.Key_Backtab: KeyMod.Shift | KeyCode.Tab,
}
KEY_FROM_QT.update(_QTONLY_KEYS)


def qmods2modelmods(modifiers: Qt.KeyboardModifier) -> KeyMod:
    """Return KeyMod from Qt.KeyboardModifier."""
    mod = KeyMod.NONE
    if modifiers & Qt.KeyboardModifier.ShiftModifier:
        mod |= KeyMod.Shift
    if modifiers & Qt.KeyboardModifier.ControlModifier:
        if mac_ctrl_meta_swapped():
            mod |= KeyMod.WinCtrl
        else:
            mod |= KeyMod.CtrlCmd
    if modifiers & Qt.KeyboardModifier.AltModifier:
        mod |= KeyMod.Alt
    if modifiers & Qt.KeyboardModifier.MetaModifier:
        if mac_ctrl_meta_swapped():
            mod |= KeyMod.CtrlCmd
        else:
            mod |= KeyMod.WinCtrl
    return mod


def qkey2modelkey(key: Qt.Key) -> KeyCode:
    """Return KeyCode from Qt.Key."""
    return KEY_FROM_QT.get(key, KeyCode.UNKOWN)


def qkeycombo2modelkey(key: QKeyCombination) -> Union[KeyCode, KeyCombo]:
    """Return KeyCode or KeyCombo from QKeyCombination."""
    if key in KEY_FROM_QT:
        return KEY_FROM_QT[key]
    qmods = _get_qmods(key)
    qkey = _get_qkey(key)
    return cast(KeyCombo, qmods2modelmods(qmods) | qkey2modelkey(qkey))


def qkeysequence2modelkeybinding(key: QKeySequence) -> KeyBinding:
    """Return KeyBinding from QKeySequence."""
    # FIXME: this should return KeyChord instead of KeyBinding... but that only takes 2
    return KeyBinding(parts=[qkeycombo2modelkey(x) for x in key])


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
