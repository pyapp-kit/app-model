from enum import Enum, auto
from collections import namedtuple
from typing import TYPE_CHECKING, Dict

if TYPE_CHECKING:
    from .._keybinding_rule import KeyBindingRule


class StandardKeyBinding(Enum):
    AddTab = auto()
    Back = auto()
    Backspace = auto()
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
    InsertLineSeparator = auto()
    InsertParagraphSeparator = auto()
    Italic = auto()
    MoveToEndOfBlock = auto()
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
    MoveToStartOfBlock = auto()
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
    SelectEndOfBlock = auto()
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
    SelectStartOfBlock = auto()
    SelectStartOfDocument = auto()
    SelectStartOfLine = auto()
    Underline = auto()
    Undo = auto()
    WhatsThis = auto()
    ZoomIn = auto()
    ZoomOut = auto()

    def to_keybinding_rule(self) -> "KeyBindingRule":
        """Return KeyBindingRule for this StandardKeyBinding."""
        from .._keybinding_rule import KeyBindingRule

        return KeyBindingRule(**_STANDARD_KEY_MAP[self])


_ = ""
SK = namedtuple("SK", "sk, win, mac, gnome")

# fmt: off
_STANDARD_KEYS = [
    SK(StandardKeyBinding.AddTab, "Ctrl+T", "Ctrl+T", "Ctrl+T"),
    SK(StandardKeyBinding.Back, "Alt+Left, Backspace", "Ctrl+[", "Alt+Left"),
    SK(StandardKeyBinding.Backspace, _, "Meta+H", _),
    SK(StandardKeyBinding.Bold, "Ctrl+B", "Ctrl+B", "Ctrl+B"),
    SK(StandardKeyBinding.Cancel, "Escape", "Escape, Ctrl+.", "Escape"),
    SK(StandardKeyBinding.Close, "Ctrl+F4, Ctrl+W", "Ctrl+W, Ctrl+F4", "Ctrl+W"),
    SK(StandardKeyBinding.Copy, "Ctrl+C, Ctrl+Ins", "Ctrl+C", "Ctrl+C, F16, Ctrl+Ins"),
    SK(StandardKeyBinding.Cut, "Ctrl+X Shift+Del", "Ctrl+X Meta+K", "Ctrl+X F20 Shift+Del"),
    SK(StandardKeyBinding.Delete, "Del", "Del, Meta+D", "Del, Ctrl+D"),
    SK(StandardKeyBinding.DeleteCompleteLine, _, _, "Ctrl+U"),
    SK(StandardKeyBinding.DeleteEndOfLine, _, _, "Ctrl+K"),
    SK(StandardKeyBinding.DeleteEndOfWord, "Ctrl+Del", _, "Ctrl+Del"),
    SK(StandardKeyBinding.DeleteStartOfWord, "Ctrl+Backspace", "Alt+Backspace", "Ctrl+Backspace"),
    SK(StandardKeyBinding.Deselect, _, _, "Ctrl+Shift+A"),
    SK(StandardKeyBinding.Find, "Ctrl+F", "Ctrl+F", "Ctrl+F"),
    SK(StandardKeyBinding.FindNext, "F3, Ctrl+G", "Ctrl+G", "Ctrl+G, F3"),
    SK(StandardKeyBinding.FindPrevious, "Shift+F3 Ctrl+Shift+G", "Ctrl+Shift+G", "Ctrl+Shift+G Shift+F3"),
    SK(StandardKeyBinding.Forward, "Alt+Right, Shift+Backspace", "Ctrl+]", "Alt+Right"),
    SK(StandardKeyBinding.FullScreen, "F11, Alt+Enter", "Ctrl+Meta+F", "Ctrl+F11"),
    SK(StandardKeyBinding.HelpContents, "F1", "Ctrl+?", "F1"),
    SK(StandardKeyBinding.InsertLineSeparator, "Shift+Enter", "Meta+Enter Meta+O", "Shift+Enter"),
    SK(StandardKeyBinding.InsertParagraphSeparator, "Enter", "Enter", "Enter"),
    SK(StandardKeyBinding.Italic, "Ctrl+I", "Ctrl+I", "Ctrl+I"),
    SK(StandardKeyBinding.MoveToEndOfBlock, _, "Alt+Down, Meta+E", _),
    SK(StandardKeyBinding.MoveToEndOfDocument, "Ctrl+End", "Ctrl+Down, End", "Ctrl+End"),
    SK(StandardKeyBinding.MoveToEndOfLine, "End", "Ctrl+Right Meta+Right", "End Ctrl+E"),
    SK(StandardKeyBinding.MoveToNextChar, "Right", "Right, Meta+F", "Right"),
    SK(StandardKeyBinding.MoveToNextLine, "Down", "Down, Meta+N", "Down"),
    SK(StandardKeyBinding.MoveToNextPage, "PgDown", "PgDown Alt+PgDown Meta+Down Meta+PgDown Meta+V", "PgDown"),
    SK(StandardKeyBinding.MoveToNextWord, "Ctrl+Right", "Alt+Right", "Ctrl+Right"),
    SK(StandardKeyBinding.MoveToPreviousChar, "Left", "Left, Meta+B", "Left"),
    SK(StandardKeyBinding.MoveToPreviousLine, "Up", "Up, Meta+P", "Up"),
    SK(StandardKeyBinding.MoveToPreviousPage, "PgUp", "PgUp Alt+PgUp Meta+Up Meta+PgUp", "PgUp"),
    SK(StandardKeyBinding.MoveToPreviousWord, "Ctrl+Left", "Alt+Left", "Ctrl+Left"),
    SK(StandardKeyBinding.MoveToStartOfBlock, _, "Alt+Up, Meta+A", _),
    SK(StandardKeyBinding.MoveToStartOfDocument, "Ctrl+Home", "Ctrl+Up Home", "Ctrl+Home"),
    SK(StandardKeyBinding.MoveToStartOfLine, "Home", "Ctrl+Left, Meta+Left", "Home"),
    SK(StandardKeyBinding.New, "Ctrl+N", "Ctrl+N", "Ctrl+N"),
    SK(StandardKeyBinding.NextChild, "Ctrl+Tab Forward Ctrl+F6", "Ctrl+} Forward Ctrl+Tab", "Ctrl+Tab Forward"),
    SK(StandardKeyBinding.Open, "Ctrl+O", "Ctrl+O", "Ctrl+O"),
    SK(StandardKeyBinding.Paste, "Ctrl+V Shift+Ins", "Ctrl+V Meta+Y", "Ctrl+V F18 Shift+Ins"),
    SK(StandardKeyBinding.Preferences, _, "Ctrl+,", _),
    SK(StandardKeyBinding.PreviousChild, "Ctrl+Shift+Tab Back Ctrl+Shift+F6", "Ctrl+{ Back Ctrl+Shift+Tab", "Ctrl+Shift+Tab Back"),
    SK(StandardKeyBinding.Print, "Ctrl+P", "Ctrl+P", "Ctrl+P"),
    SK(StandardKeyBinding.Quit, _, "Ctrl+Q", "Ctrl+Q"),
    SK(StandardKeyBinding.Redo, "Ctrl+Y Shift+Ctrl+Z Alt+Shift+Backspace", "Ctrl+Shift+Z", "Ctrl+Shift+Z"),
    SK(StandardKeyBinding.Refresh, "F5", "F5", "Ctrl+R, F5"),
    SK(StandardKeyBinding.Replace, "Ctrl+H", _, "Ctrl+H"),
    SK(StandardKeyBinding.Save, "Ctrl+S", "Ctrl+S", "Ctrl+S"),
    SK(StandardKeyBinding.SaveAs, _, "Ctrl+Shift+S", "Ctrl+Shift+S"),
    SK(StandardKeyBinding.SelectAll, "Ctrl+A", "Ctrl+A", "Ctrl+A"),
    SK(StandardKeyBinding.SelectEndOfBlock, _, "Alt+Shift+Down Meta+Shift+E", _),
    SK(StandardKeyBinding.SelectEndOfDocument, "Ctrl+Shift+End", "Ctrl+Shift+Down Shift+End", "Ctrl+Shift+End"),
    SK(StandardKeyBinding.SelectEndOfLine, "Shift+End", "Ctrl+Shift+Right", "Shift+End"),
    SK(StandardKeyBinding.SelectNextChar, "Shift+Right", "Shift+Right", "Shift+Right"),
    SK(StandardKeyBinding.SelectNextLine, "Shift+Down", "Shift+Down", "Shift+Down"),
    SK(StandardKeyBinding.SelectNextPage, "Shift+PgDown", "Shift+PgDown", "Shift+PgDown"),
    SK(StandardKeyBinding.SelectNextWord, "Ctrl+Shift+Right", "Alt+Shift+Right", "Ctrl+Shift+Right"),
    SK(StandardKeyBinding.SelectPreviousChar, "Shift+Left", "Shift+Left", "Shift+Left"),
    SK(StandardKeyBinding.SelectPreviousLine, "Shift+Up", "Shift+Up", "Shift+Up"),
    SK(StandardKeyBinding.SelectPreviousPage, "Shift+PgUp", "Shift+PgUp", "Shift+PgUp"),
    SK(StandardKeyBinding.SelectPreviousWord, "Ctrl+Shift+Left", "Alt+Shift+Left", "Ctrl+Shift+Left"),
    SK(StandardKeyBinding.SelectStartOfBlock, _, "Alt+Shift+Up Meta+Shift+A", _),
    SK(StandardKeyBinding.SelectStartOfDocument, "Ctrl+Shift+Home", "Ctrl+Shift+Up Shift+Home", "Ctrl+Shift+Home"),
    SK(StandardKeyBinding.SelectStartOfLine, "Shift+Home", "Ctrl+Shift+Left", "Shift+Home"),
    SK(StandardKeyBinding.Underline, "Ctrl+U", "Ctrl+U", "Ctrl+U"),
    SK(StandardKeyBinding.Undo, "Ctrl+Z, Alt+Backspace", "Ctrl+Z", "Ctrl+Z, F14"),
    SK(StandardKeyBinding.WhatsThis, "Shift+F1", "Shift+F1", "Shift+F1"),
    SK(StandardKeyBinding.ZoomIn, "Ctrl+Plus", "Ctrl+Plus", "Ctrl+Plus"),
    SK(StandardKeyBinding.ZoomOut, "Ctrl+Minus", "Ctrl+Minus", "Ctrl+Minus"),
]

# fmt: on
_STANDARD_KEY_MAP: Dict[StandardKeyBinding, Dict[str, str]] = {
    nt.sk: {"win": nt.win, "mac": nt.mac, "linux": nt.gnome} for nt in _STANDARD_KEYS
}
