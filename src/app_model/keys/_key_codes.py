from enum import IntEnum, auto


class KeyCode(IntEnum):
    DependsOnKbLayout = -1
    Unknown = 0

    Backspace = auto()
    Tab = auto()
    Enter = auto()
    Shift = auto()
    Ctrl = auto()
    Alt = auto()
    PauseBreak = auto()
    CapsLock = auto()
    Escape = auto()
    Space = auto()
    PageUp = auto()
    PageDown = auto()
    End = auto()
    Home = auto()
    LeftArrow = auto()
    UpArrow = auto()
    RightArrow = auto()
    DownArrow = auto()
    Insert = auto()
    Delete = auto()

    Digit0 = auto()
    Digit1 = auto()
    Digit2 = auto()
    Digit3 = auto()
    Digit4 = auto()
    Digit5 = auto()
    Digit6 = auto()
    Digit7 = auto()
    Digit8 = auto()
    Digit9 = auto()

    KeyA = auto()
    KeyB = auto()
    KeyC = auto()
    KeyD = auto()
    KeyE = auto()
    KeyF = auto()
    KeyG = auto()
    KeyH = auto()
    KeyI = auto()
    KeyJ = auto()
    KeyK = auto()
    KeyL = auto()
    KeyM = auto()
    KeyN = auto()
    KeyO = auto()
    KeyP = auto()
    KeyQ = auto()
    KeyR = auto()
    KeyS = auto()
    KeyT = auto()
    KeyU = auto()
    KeyV = auto()
    KeyW = auto()
    KeyX = auto()
    KeyY = auto()
    KeyZ = auto()

    Meta = auto()
    ContextMenu = auto()

    F1 = auto()
    F2 = auto()
    F3 = auto()
    F4 = auto()
    F5 = auto()
    F6 = auto()
    F7 = auto()
    F8 = auto()
    F9 = auto()
    F10 = auto()
    F11 = auto()
    F12 = auto()
    F13 = auto()
    F14 = auto()
    F15 = auto()
    F16 = auto()
    F17 = auto()
    F18 = auto()
    F19 = auto()

    NumLock = auto()
    ScrollLock = auto()

    # Used for miscellaneous characters; it can vary by keyboard.
    # For the US standard keyboard, the ';:' key
    Semicolon = auto()
    # For any country/region, the '+' key
    # For the US standard keyboard, the '=+' key
    Equal = auto()
    # For any country/region, the ',' key
    # For the US standard keyboard, the ',<' key
    Comma = auto()
    # For any country/region, the '-' key
    # For the US standard keyboard, the '-_' key
    Minus = auto()
    # For any country/region, the '.' key
    # For the US standard keyboard, the '.>' key
    Period = auto()
    # Used for miscellaneous characters; it can vary by keyboard.
    # For the US standard keyboard, the '/?' key
    Slash = auto()
    # Used for miscellaneous characters; it can vary by keyboard.
    # For the US standard keyboard, the '`~' key
    Backquote = auto()
    # Used for miscellaneous characters; it can vary by keyboard.
    # For the US standard keyboard, the '[{' key
    BracketLeft = auto()
    # Used for miscellaneous characters; it can vary by keyboard.
    # For the US standard keyboard, the '\|' key
    Backslash = auto()
    # Used for miscellaneous characters; it can vary by keyboard.
    # For the US standard keyboard, the ']}' key
    BracketRight = auto()
    # Used for miscellaneous characters; it can vary by keyboard.
    # For the US standard keyboard, the ''"' key
    Quote = auto()

    # Either the angle bracket key or the backslash key on the RT 102-key keyboard.
    IntlBackslash = auto()

    Numpad0 = auto()  # VK_NUMPAD0, 0x60, Numeric keypad 0 key
    Numpad1 = auto()  # VK_NUMPAD1, 0x61, Numeric keypad 1 key
    Numpad2 = auto()  # VK_NUMPAD2, 0x62, Numeric keypad 2 key
    Numpad3 = auto()  # VK_NUMPAD3, 0x63, Numeric keypad 3 key
    Numpad4 = auto()  # VK_NUMPAD4, 0x64, Numeric keypad 4 key
    Numpad5 = auto()  # VK_NUMPAD5, 0x65, Numeric keypad 5 key
    Numpad6 = auto()  # VK_NUMPAD6, 0x66, Numeric keypad 6 key
    Numpad7 = auto()  # VK_NUMPAD7, 0x67, Numeric keypad 7 key
    Numpad8 = auto()  # VK_NUMPAD8, 0x68, Numeric keypad 8 key
    Numpad9 = auto()  # VK_NUMPAD9, 0x69, Numeric keypad 9 key

    NumpadMultiply = auto()  # VK_MULTIPLY, 0x6A, Multiply key
    NumpadAdd = auto()  # VK_ADD, 0x6B, Add key
    NUMPAD_SEPARATOR = auto()  # VK_SEPARATOR, 0x6C, Separator key
    NumpadSubtract = auto()  # VK_SUBTRACT, 0x6D, Subtract key
    NumpadDecimal = auto()  # VK_DECIMAL, 0x6E, Decimal key
    NumpadDivide = auto()  # VK_DIVIDE, 0x6F,


class KeyMod(IntEnum):
    WinCtrl = 2**8
    Alt = 2**9
    Shift = 2**10
    CtrlCmd = 2**11


class KeyChord(int):
    def __new__(cls, first_part: int, second_part: int):
        chord_part = ((second_part & 0x0000FFFF) << 16) >> 0
        obj = super().__new__(cls, (first_part | chord_part) >> 0)
        setattr(obj, "_chord_part", chord_part)
        return obj

    def __init__(self, first_part: int, second_part: int):
        self._first_part = first_part
        self._second_part = second_part

    def __repr__(self) -> str:
        return f"KeyChord({self._first_part}, {self._second_part})"
