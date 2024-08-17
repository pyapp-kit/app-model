from collections import namedtuple
from enum import Enum, auto
from typing import TYPE_CHECKING, Dict

from ._key_codes import KeyCode, KeyMod

if TYPE_CHECKING:
    from .._keybinding_rule import KeyBindingRule


class StandardKeyBinding(Enum):
    AddTab = auto()
    Back = auto()
    Bold = auto()
    Cancel = auto()
    Close = auto()
    Copy = auto()
    Cut = auto()
    Delete = auto()
    DeleteCompleteLine = auto()
    DeleteEndOfLine = auto()
    DeleteEndOfWord = auto()
    DeleteStartOfWord = auto()
    Deselect = auto()
    Find = auto()
    FindNext = auto()
    FindPrevious = auto()
    Forward = auto()
    FullScreen = auto()
    HelpContents = auto()
    Italic = auto()
    MoveToEndOfDocument = auto()
    MoveToEndOfLine = auto()
    MoveToNextChar = auto()
    MoveToNextLine = auto()
    MoveToNextPage = auto()
    MoveToNextWord = auto()
    MoveToPreviousChar = auto()
    MoveToPreviousLine = auto()
    MoveToPreviousPage = auto()
    MoveToPreviousWord = auto()
    MoveToStartOfDocument = auto()
    MoveToStartOfLine = auto()
    New = auto()
    NextChild = auto()
    Open = auto()
    Paste = auto()
    Preferences = auto()
    PreviousChild = auto()
    Print = auto()
    Quit = auto()
    Redo = auto()
    Refresh = auto()
    Replace = auto()
    Save = auto()
    SaveAs = auto()
    SelectAll = auto()
    SelectEndOfDocument = auto()
    SelectEndOfLine = auto()
    SelectNextChar = auto()
    SelectNextLine = auto()
    SelectNextPage = auto()
    SelectNextWord = auto()
    SelectPreviousChar = auto()
    SelectPreviousLine = auto()
    SelectPreviousPage = auto()
    SelectPreviousWord = auto()
    SelectStartOfDocument = auto()
    SelectStartOfLine = auto()
    Underline = auto()
    Undo = auto()
    WhatsThis = auto()
    OriginalSize = auto()
    ZoomIn = auto()
    ZoomOut = auto()

    def to_keybinding_rule(self) -> "KeyBindingRule":
        """Return KeyBindingRule for this StandardKeyBinding."""
        from .._keybinding_rule import KeyBindingRule

        return KeyBindingRule(**_STANDARD_KEY_MAP[self])


_ = None
SK = namedtuple("SK", "sk, primary, win, mac, gnome", defaults=(_, _, _, _, _))

# fmt: off
# flake8: noqa

_STANDARD_KEYS = [
    SK(StandardKeyBinding.AddTab, KeyMod.CtrlCmd | KeyCode.KeyT),
    SK(StandardKeyBinding.Back, KeyMod.Alt | KeyCode.LeftArrow, _, KeyMod.CtrlCmd | KeyCode.BracketLeft),
    SK(StandardKeyBinding.Bold, KeyMod.CtrlCmd | KeyCode.KeyB),
    SK(StandardKeyBinding.Cancel, KeyCode.Escape),
    SK(StandardKeyBinding.Close, KeyMod.CtrlCmd | KeyCode.KeyW),
    SK(StandardKeyBinding.Copy, KeyMod.CtrlCmd | KeyCode.KeyC),
    SK(StandardKeyBinding.Cut, KeyMod.CtrlCmd | KeyCode.KeyX),
    SK(StandardKeyBinding.Delete, KeyCode.Delete),
    SK(StandardKeyBinding.DeleteCompleteLine, _, _, _, KeyMod.CtrlCmd | KeyCode.KeyU),
    SK(StandardKeyBinding.DeleteEndOfLine, _, _, _, KeyMod.CtrlCmd | KeyCode.KeyK),
    SK(StandardKeyBinding.DeleteEndOfWord, _, KeyMod.CtrlCmd | KeyCode.Delete, _, KeyMod.CtrlCmd | KeyCode.Delete),
    SK(StandardKeyBinding.DeleteStartOfWord, _, KeyMod.CtrlCmd | KeyCode.Backspace, KeyMod.Alt | KeyCode.Backspace, KeyMod.CtrlCmd | KeyCode.Backspace),
    SK(StandardKeyBinding.Deselect, _, _, _, KeyMod.CtrlCmd | KeyMod.Shift | KeyCode.KeyA),
    SK(StandardKeyBinding.Find, KeyMod.CtrlCmd | KeyCode.KeyF),
    SK(StandardKeyBinding.FindNext, KeyMod.CtrlCmd | KeyCode.KeyG),
    SK(StandardKeyBinding.FindPrevious, KeyMod.CtrlCmd | KeyMod.Shift | KeyCode.KeyG),
    SK(StandardKeyBinding.Forward, _, KeyMod.Alt | KeyCode.RightArrow, KeyMod.CtrlCmd | KeyCode.BracketRight, KeyMod.Alt | KeyCode.RightArrow),
    SK(StandardKeyBinding.FullScreen, _, KeyMod.Alt | KeyCode.Enter, KeyMod.WinCtrl | KeyMod.CtrlCmd | KeyCode.KeyF, KeyMod.CtrlCmd | KeyCode.F11),
    SK(StandardKeyBinding.HelpContents, KeyCode.F1, _, KeyMod.CtrlCmd | KeyCode.Slash),
    SK(StandardKeyBinding.Italic, KeyMod.CtrlCmd | KeyCode.KeyI),
    SK(StandardKeyBinding.MoveToEndOfDocument, KeyMod.CtrlCmd | KeyCode.End, _, KeyMod.CtrlCmd | KeyCode.DownArrow),
    SK(StandardKeyBinding.MoveToEndOfLine, KeyCode.End, _, KeyMod.CtrlCmd | KeyCode.RightArrow),
    SK(StandardKeyBinding.MoveToNextChar, KeyCode.RightArrow),
    SK(StandardKeyBinding.MoveToNextLine, KeyCode.DownArrow),
    SK(StandardKeyBinding.MoveToNextPage, KeyCode.PageDown),
    SK(StandardKeyBinding.MoveToNextWord, KeyMod.CtrlCmd | KeyCode.RightArrow, _, KeyMod.Alt | KeyCode.RightArrow),
    SK(StandardKeyBinding.MoveToPreviousChar, KeyCode.LeftArrow),
    SK(StandardKeyBinding.MoveToPreviousLine, KeyCode.UpArrow),
    SK(StandardKeyBinding.MoveToPreviousPage, KeyCode.PageUp),
    SK(StandardKeyBinding.MoveToPreviousWord, KeyMod.CtrlCmd | KeyCode.LeftArrow, _, KeyMod.Alt | KeyCode.LeftArrow),
    SK(StandardKeyBinding.MoveToStartOfDocument, KeyMod.CtrlCmd | KeyCode.Home, _, KeyCode.Home),
    SK(StandardKeyBinding.MoveToStartOfLine, KeyCode.Home, _, KeyMod.CtrlCmd | KeyCode.LeftArrow),
    SK(StandardKeyBinding.New, KeyMod.CtrlCmd | KeyCode.KeyN),
    SK(StandardKeyBinding.NextChild, KeyMod.CtrlCmd | KeyCode.Tab, _, KeyMod.CtrlCmd | KeyMod.Shift | KeyCode.BracketRight),
    SK(StandardKeyBinding.Open, KeyMod.CtrlCmd | KeyCode.KeyO),
    SK(StandardKeyBinding.Paste, KeyMod.CtrlCmd | KeyCode.KeyV),
    SK(StandardKeyBinding.Preferences, KeyMod.CtrlCmd | KeyCode.Comma),
    SK(StandardKeyBinding.PreviousChild, KeyMod.CtrlCmd | KeyMod.Shift | KeyCode.Tab, _, KeyMod.CtrlCmd | KeyMod.Shift | KeyCode.BracketLeft),
    SK(StandardKeyBinding.Print, KeyMod.CtrlCmd | KeyCode.KeyP),
    SK(StandardKeyBinding.Quit, KeyMod.CtrlCmd | KeyCode.KeyQ),
    SK(StandardKeyBinding.Redo, KeyMod.CtrlCmd | KeyMod.Shift | KeyCode.KeyZ, KeyMod.CtrlCmd | KeyCode.KeyY),
    SK(StandardKeyBinding.Refresh, KeyMod.CtrlCmd | KeyCode.KeyR),
    SK(StandardKeyBinding.Replace, KeyMod.CtrlCmd | KeyCode.KeyH),
    SK(StandardKeyBinding.Save, KeyMod.CtrlCmd | KeyCode.KeyS),
    SK(StandardKeyBinding.SaveAs, KeyMod.CtrlCmd | KeyMod.Shift | KeyCode.KeyS),
    SK(StandardKeyBinding.SelectAll, KeyMod.CtrlCmd | KeyCode.KeyA),
    SK(StandardKeyBinding.SelectEndOfDocument, KeyMod.CtrlCmd | KeyMod.Shift | KeyCode.End),
    SK(StandardKeyBinding.SelectEndOfLine, KeyMod.Shift | KeyCode.End, _, KeyMod.CtrlCmd | KeyMod.Shift | KeyCode.RightArrow),
    SK(StandardKeyBinding.SelectNextChar, KeyMod.Shift | KeyCode.RightArrow),
    SK(StandardKeyBinding.SelectNextLine,  KeyMod.Shift | KeyCode.DownArrow),
    SK(StandardKeyBinding.SelectNextPage,  KeyMod.Shift | KeyCode.PageDown),
    SK(StandardKeyBinding.SelectNextWord, KeyMod.CtrlCmd | KeyMod.Shift | KeyCode.RightArrow, _, KeyMod.Alt | KeyMod.Shift | KeyCode.RightArrow),
    SK(StandardKeyBinding.SelectPreviousChar, KeyMod.Shift | KeyCode.LeftArrow),
    SK(StandardKeyBinding.SelectPreviousLine, KeyMod.Shift | KeyCode.UpArrow),
    SK(StandardKeyBinding.SelectPreviousPage, KeyMod.Shift | KeyCode.PageUp),
    SK(StandardKeyBinding.SelectPreviousWord, KeyMod.CtrlCmd | KeyMod.Shift | KeyCode.LeftArrow, _, KeyMod.Alt | KeyMod.Shift | KeyCode.LeftArrow),
    SK(StandardKeyBinding.SelectStartOfDocument, KeyMod.CtrlCmd | KeyMod.Shift | KeyCode.Home),
    SK(StandardKeyBinding.SelectStartOfLine, KeyMod.Shift | KeyCode.Home, _, KeyMod.CtrlCmd | KeyMod.Shift | KeyCode.LeftArrow),
    SK(StandardKeyBinding.Underline, KeyMod.CtrlCmd | KeyCode.KeyU),
    SK(StandardKeyBinding.Undo, KeyMod.CtrlCmd | KeyCode.KeyZ),
    SK(StandardKeyBinding.WhatsThis, KeyMod.Shift | KeyCode.F1),
    SK(StandardKeyBinding.OriginalSize, KeyMod.CtrlCmd | KeyCode.Digit0),
    SK(StandardKeyBinding.ZoomIn, KeyMod.CtrlCmd | KeyCode.Equal),
    SK(StandardKeyBinding.ZoomOut, KeyMod.CtrlCmd | KeyCode.Minus),
]

# fmt: on
_STANDARD_KEY_MAP: Dict[StandardKeyBinding, Dict[str, str]] = {
    nt.sk: {"primary": nt.primary, "win": nt.win, "mac": nt.mac, "linux": nt.gnome}
    for nt in _STANDARD_KEYS
}
