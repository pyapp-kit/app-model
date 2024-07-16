from enum import IntEnum, IntFlag, auto
from typing import (
    TYPE_CHECKING,
    Any,
    Callable,
    Dict,
    Generator,
    NamedTuple,
    Optional,
    Set,
    Tuple,
    Type,
    Union,
    overload,
)

from app_model.types._constants import OperatingSystem

if TYPE_CHECKING:
    from pydantic.annotated_handlers import GetCoreSchemaHandler
    from pydantic_core import core_schema

__all__ = ["KeyCode", "KeyMod", "ScanCode", "KeyChord"]

# TODO:
# https://stackoverflow.com/questions/3202629/where-can-i-find-a-list-of-mac-virtual-key-codes/16125341#16125341

# flake8: noqa
# fmt: off


class KeyCode(IntEnum):
    """Virtual Key Codes, the integer value does not hold any inherent meaning.

    This is the primary internal representation of a key.
    """

    UNKNOWN = 0

    # -----------------------   Writing System Keys   -----------------------
    Backquote = auto()		#	`~ on a US keyboard.
    Backslash = auto()      #	\| on a US keyboard.
    BracketLeft = auto()    #	[{ on a US keyboard.
    BracketRight = auto()   #	]} on a US keyboard.
    Comma = auto()			#	,< on a US keyboard.
    Digit0 = auto()			#	0) on a US keyboard.
    Digit1 = auto()			#	1! on a US keyboard.
    Digit2 = auto()			#	2@ on a US keyboard.
    Digit3 = auto()			#	3# on a US keyboard.
    Digit4 = auto()			#	4$ on a US keyboard.
    Digit5 = auto()			#	5% on a US keyboard.
    Digit6 = auto()			#	6^ on a US keyboard.
    Digit7 = auto()			#	7& on a US keyboard.
    Digit8 = auto()			#	8* on a US keyboard.
    Digit9 = auto()			#	9( on a US keyboard.
    Equal = auto()			#	=+ on a US keyboard.
    IntlBackslash = auto()	#	Located between the left Shift and Z keys. Labelled \| on a UK keyboard.
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
    Minus = auto()			#	-_ on a US keyboard.
    Period = auto()			#	.> on a US keyboard.
    Quote = auto()			#	'" on a US keyboard.
    Semicolon = auto()		#	;: on a US keyboard.
    Slash = auto()			#	/? on a US keyboard.

    # -------------------   Functional Keys   --------------------------------
    Alt = auto()		    # Alt, Option or ⌥.
    Backspace = auto()		# Backspace or ⌫. Labelled Delete on Apple keyboards.
    CapsLock = auto()		# CapsLock or ⇪
    ContextMenu = auto()	# The application context menu key, which is typically found between the right Meta key and the right Control key.
    Ctrl = auto()	        # Control or ⌃
    Enter = auto()		    # Enter or ↵. Labelled Return on Apple keyboards.
    Meta = auto()		    # The Windows, ⌘, Command or other OS symbol key.
    Shift = auto()		    # Shift or ⇧
    Space = auto()		    # (space)
    Tab = auto()		    # Tab or ⇥

    # ----------------------   Control Pad   --------------------------------

    Delete = auto()         # ⌦. The forward delete key. NOT the Delete key on a mac
    End = auto()            # Page Down, End or ↘
    Home = auto()           # Home or ↖
    Insert = auto()         # Insert or Ins. Not present on Apple keyboards.
    PageDown = auto()       # Page Down, PgDn or ⇟
    PageUp = auto()         # Page Up, PgUp or ⇞

    # -----------------------   Arrow Pad   ----------------------------------

    DownArrow = auto()      # ↓
    LeftArrow = auto()      # ←
    RightArrow = auto()     # →
    UpArrow = auto()        # ↑

    # -----------------------   Numpad Section   -----------------------------

    NumLock = auto()            #
    Numpad0 = auto()            # 0
    Numpad1 = auto()            # 1
    Numpad2 = auto()            # 2
    Numpad3 = auto()            # 3
    Numpad4 = auto()            # 4
    Numpad5 = auto()            # 5
    Numpad6 = auto()            # 6
    Numpad7 = auto()            # 7
    Numpad8 = auto()            # 8
    Numpad9 = auto()            # 9
    NumpadAdd = auto()          # +
    NumpadDecimal = auto()      # .
    NumpadDivide = auto()       # /
    NumpadMultiply = auto()     # *
    NumpadSubtract = auto()     # -

    # ---------------------   Function Section   -----------------------------

    Escape = auto() 	        # Esc or ⎋
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
    PrintScreen = auto()
    ScrollLock = auto()
    PauseBreak = auto()

    def __str__(self) -> str:
        """Get a normalized string representation (constant to all OSes) of this `KeyCode`."""
        return keycode_to_string(self)

    def os_symbol(self, os: Optional[OperatingSystem] = None) -> str:
        """Get a string representation of this `KeyCode` using a symbol/OS specific symbol.

        Some examples:
            * `KeyCode.Enter` is represented by `↵`
            * `KeyCode.Meta` is represented by `⊞` on Windows, `Super` on Linux and `⌘` on MacOS

        If no OS is given, the current detected one is used.
        """
        os = OperatingSystem.current() if os is None else os
        return keycode_to_os_symbol(self, os)

    def os_name(self, os: Optional[OperatingSystem] = None) -> str:
        """Get a string representation of this `KeyCode` using the OS specific naming for the key.

        This differs from `__str__` since with it a normalized representation (constant to all OSes) is given.
        Sometimes these representations coincide but not always! Some examples:
            * `KeyCode.Enter` is represented by `Enter` (`__str__` represents it as `Enter`)
            * `KeyCode.Meta` is represented by `Win` on Windows, `Super` on Linux and `Cmd` on MacOS
            (`__str__` represents it as `Meta`)

        If no OS is given, the current detected one is used.
        """
        os = OperatingSystem.current() if os is None else os
        return keycode_to_os_name(self, os)

    @classmethod
    def from_string(cls, string: str) -> 'KeyCode':
        """Return the `KeyCode` associated with the given string.

        Returns `KeyCode.UNKNOWN` if no `KeyCode` is associated with the string.
        """
        return keycode_from_string(string)

    @classmethod
    def from_event_code(cls, event_code: int) -> 'KeyCode':
        """Return the `KeyCode` associated with the given event code.

        Returns `KeyCode.UNKNOWN` if no `KeyCode` is associated with the event code.
        """
        return _EVENTCODE_TO_KEYCODE.get(event_code, KeyCode.UNKNOWN)

    @classmethod
    def __get_validators__(cls) -> Generator[Callable[..., 'KeyCode'], None, None]:
        yield cls.validate

    @classmethod
    def __get_pydantic_core_schema__(
        cls, source: type, handler: 'GetCoreSchemaHandler'
    ) -> 'core_schema.CoreSchema':
        from pydantic_core import core_schema

        return core_schema.no_info_plain_validator_function(cls.validate)

    @classmethod
    def validate(cls, value: Any) -> 'KeyCode':
        if isinstance(value, KeyCode):
            return value
        if isinstance(value, int):
            return cls(value)
        if isinstance(value, str):
            return cls.from_string(value)
        raise TypeError(f'cannot convert type {type(value)!r} to KeyCode')


class ScanCode(IntEnum):
    """Scan codes for the keyboard.

    https://en.wikipedia.org/wiki/Scancode

    These are the scan codes required to conform to the W3C specification for
    KeyboardEvent.code
    
    A scan code is a hardware-specific code that is generated by the keyboard when a key
    is pressed or released. It represents the physical location of a key on the keyboard
    and is unique to each key. A key code, on the other hand, is a higher-level
    representation of a keypress or key release event. They are associated with
    characters, functions, or actions rather than hardware locations.
    As an example, the left and right control keys have the same key code (KeyCode.Ctrl)
    but different scan codes (LeftControl and RightControl).

    https://w3c.github.io/uievents-code/

    commented out lines represent keys that  are optional and may be used by
    implementations to support special keyboards (such as multimedia or
    legacy keyboards).
    """

    UNIDENTIFIED = 0        # This value code should be used when no other value given in this specification is appropriate.

    # -----------------------   Writing System Keys   -----------------------
    # https://w3c.github.io/uievents-code/#key-alphanumeric-writing-system
    # The writing system keys are those that change meaning (i.e., they produce
    # different key values) based on the current locale and keyboard layout.
    # ----------------------------------------------------------------------

    Backquote = auto()		#	`~ on a US keyboard. This is the 半角/全角/漢字 (hankaku/zenkaku/kanji) key on Japanese keyboards
    Backslash = auto()      #	Used for both the US \| (on the 101-key layout) and also for the key located between the " and Enter keys on row C of the 102-, 104- and 106-key layouts. Labelled #~ on a UK (102) keyboard.
    BracketLeft = auto()    #	[{ on a US keyboard.
    BracketRight = auto()   #	]} on a US keyboard.
    Comma = auto()			#	,< on a US keyboard.
    Digit0 = auto()			#	0) on a US keyboard.
    Digit1 = auto()			#	1! on a US keyboard.
    Digit2 = auto()			#	2@ on a US keyboard.
    Digit3 = auto()			#	3# on a US keyboard.
    Digit4 = auto()			#	4$ on a US keyboard.
    Digit5 = auto()			#	5% on a US keyboard.
    Digit6 = auto()			#	6^ on a US keyboard.
    Digit7 = auto()			#	7& on a US keyboard.
    Digit8 = auto()			#	8* on a US keyboard.
    Digit9 = auto()			#	9( on a US keyboard.
    Equal = auto()			#	=+ on a US keyboard.
    IntlBackslash = auto()	#	Located between the left Shift and Z keys. Labelled \| on a UK keyboard.
    IntlRo = auto()			#	Located between the / and right Shift keys. Labelled \ろ (ro) on a Japanese keyboard.
    IntlYen = auto()		#	Located between the = and Backspace keys. Labelled ¥ (yen) on a Japanese keyboard. \/ on a Russian keyboard.
    KeyA = auto()			#	a on a US keyboard. Labelled q on an AZERTY (e.g., French) keyboard.
    KeyB = auto()			#	b on a US keyboard.
    KeyC = auto()			#	c on a US keyboard.
    KeyD = auto()			#	d on a US keyboard.
    KeyE = auto()			#	e on a US keyboard.
    KeyF = auto()			#	f on a US keyboard.
    KeyG = auto()			#	g on a US keyboard.
    KeyH = auto()			#	h on a US keyboard.
    KeyI = auto()			#	i on a US keyboard.
    KeyJ = auto()			#	j on a US keyboard.
    KeyK = auto()			#	k on a US keyboard.
    KeyL = auto()			#	l on a US keyboard.
    KeyM = auto()			#	m on a US keyboard.
    KeyN = auto()			#	n on a US keyboard.
    KeyO = auto()			#	o on a US keyboard.
    KeyP = auto()			#	p on a US keyboard.
    KeyQ = auto()			#	q on a US keyboard. Labelled a on an AZERTY (e.g., French) keyboard.
    KeyR = auto()			#	r on a US keyboard.
    KeyS = auto()			#	s on a US keyboard.
    KeyT = auto()			#	t on a US keyboard.
    KeyU = auto()			#	u on a US keyboard.
    KeyV = auto()			#	v on a US keyboard.
    KeyW = auto()			#	w on a US keyboard. Labelled z on an AZERTY (e.g., French) keyboard.
    KeyX = auto()			#	x on a US keyboard.
    KeyY = auto()			#	y on a US keyboard. Labelled z on a QWERTZ (e.g., German) keyboard.
    KeyZ = auto()			#	z on a US keyboard. Labelled w on an AZERTY (e.g., French) keyboard, and y on a QWERTZ (e.g., German) keyboard.
    Minus = auto()			#	-_ on a US keyboard.
    Period = auto()			#	.> on a US keyboard.
    Quote = auto()			#	'" on a US keyboard.
    Semicolon = auto()		#	;: on a US keyboard.
    Slash = auto()			#	/? on a US keyboard.

    # -------------------   Functional Keys   --------------------------------
    # https://w3c.github.io/uievents-code/#key-alphanumeric-functional
    # The functional keys (not to be confused with the function keys described later)
    # are those keys in the alphanumeric section that provide general editing functions
    # that are common to all locales (like Shift, Tab, Enter and Backspace).
    # With a few exceptions, these keys do not change meaning based on the current
    # keyboard layout.
    # ------------------------------------------------------------------------

    AltLeft = auto()		# Alt, Option or ⌥.
    AltRight = auto()		# Alt, Option or ⌥. This is labelled AltGr key on many keyboard layouts.
    Backspace = auto()		# Backspace or ⌫. Labelled Delete on Apple keyboards.
    CapsLock = auto()		# CapsLock or ⇪
    ContextMenu = auto()	# The application context menu key, which is typically found between the right Meta key and the right Control key.
    ControlLeft = auto()	# Control or ⌃
    ControlRight = auto()	# Control or ⌃
    Enter = auto()		    # Enter or ↵. Labelled Return on Apple keyboards.
    MetaLeft = auto()		# The Windows, ⌘, Command or other OS symbol key.
    MetaRight = auto()		# The Windows, ⌘, Command or other OS symbol key.
    ShiftLeft = auto()		# Shift or ⇧
    ShiftRight = auto()		# Shift or ⇧
    Space = auto()		    # (space)
    Tab = auto()		    # Tab or ⇥
    # Japanese and Korean keyboards.
    Convert = auto()		# Japanese: 変換 (henkan)
    KanaMode = auto()		# Japanese: カタカナ/ひらがな/ローマ字 (katakana/hiragana/romaji)
    NonConvert = auto()		# Japanese: 無変換 (muhenkan)
    # Lang1 = auto()		# Korean: HangulMode 한/영 (han/yeong) Japanese (Mac keyboard): かな (kana)
    # Lang2 = auto()		# Korean: Hanja 한자 (hanja) Japanese (Mac keyboard): 英数 (eisu)
    # Lang3 = auto()		# Japanese (word-processing keyboard): Katakana
    # Lang4 = auto()		# Japanese (word-processing keyboard): Hiragana
    # Lang5 = auto()		# Japanese (word-processing keyboard): Zenkaku/Hankaku

    # ----------------------   Control Pad   --------------------------------
    # https://w3c.github.io/uievents-code/#key-controlpad-section
    # The control pad section of the keyboard is the set of (usually 6) keys that
    # perform navigating and editing operations, for example, Home, PageUp and Insert.
    # ------------------------------------------------------------------------

    Delete = auto()         # ⌦. The forward delete key. Note that on Apple keyboards, the key labelled Delete on the main part of the keyboard should be encoded as "Backspace".
    End = auto()            # Page Down, End or ↘
    Help = auto()           # Help. Not present on standard PC keyboards.
    Home = auto()           # Home or ↖
    Insert = auto()         # Insert or Ins. Not present on Apple keyboards.
    PageDown = auto()       # Page Down, PgDn or ⇟
    PageUp = auto()         # Page Up, PgUp or ⇞

    # -----------------------   Arrow Pad   ----------------------------------
    # https://w3c.github.io/uievents-code/#key-arrowpad-section
    # The arrow pad contains the 4 arrow keys. The keys are commonly arranged in an
    # "upside-down T" configuration.
    # ------------------------------------------------------------------------

    ArrowDown = auto()      # ↓
    ArrowLeft = auto()      # ←
    ArrowRight = auto()     # →
    ArrowUp = auto()        # ↑

    # -----------------------   Numpad Section   -----------------------------
    # https://w3c.github.io/uievents-code/#key-numpad-section
    # The numpad section is the set of keys on the keyboard arranged in a grid like a
    # calculator or mobile phone. This section contains numeric and mathematical
    # operator keys. Laptop computers and compact keyboards will commonly omit
    # these keys to save space.
    # ------------------------------------------------------------------------

    NumLock = auto()                # On the Mac, the "NumLock" code should be used for the numpad Clear key.
    Numpad0 = auto()                # 0 Ins on a keyboard 0 on a phone or remote control
    Numpad1 = auto()                # 1 End on a keyboard 1 or 1 QZ on a phone or remote control
    Numpad2 = auto()                # 2 ↓ on a keyboard 2 ABC on a phone or remote control
    Numpad3 = auto()                # 3 PgDn on a keyboard 3 DEF on a phone or remote control
    Numpad4 = auto()                # 4 ← on a keyboard 4 GHI on a phone or remote control
    Numpad5 = auto()                # 5 on a keyboard 5 JKL on a phone or remote control
    Numpad6 = auto()                # 6 → on a keyboard 6 MNO on a phone or remote control
    Numpad7 = auto()                # 7 Home on a keyboard 7 PQRS or 7 PRS on a phone or remote control
    Numpad8 = auto()                # 8 ↑ on a keyboard 8 TUV on a phone or remote control
    Numpad9 = auto()                # 9 PgUp on a keyboard 9 WXYZ or 9 WXY on a phone or remote control
    NumpadAdd = auto()              # +
    NumpadDecimal = auto()          # . Del. For locales where the decimal separator is "," (e.g., Brazil), this key may generate a ,.
    NumpadDivide = auto()           # /
    NumpadEnter = auto()            #
    NumpadMultiply = auto()         # * on a keyboard. For use with numpads that provide mathematical operations (+, -, * and /). Use  "NumpadStar" for the * key on phones and remote controls.
    NumpadSubtract = auto()         # -
    NumpadEqual = auto()            # =  NOTE: not required to conform to spec.
    # NumpadBackspace = auto()      # Found on the Microsoft Natural Keyboard.
    # NumpadClear = auto()          # C or AC (All Clear). Also for use with numpads that have a Clear key that is separate from the NumLock key. On the Mac, the numpad Clear key should always be encoded as "NumLock".
    # NumpadClearEntry = auto()     # CE (Clear Entry)
    # NumpadComma = auto()          # , (thousands separator). For locales where the thousands separator is a "." (e.g., Brazil), this key may generate a ..
    # NumpadHash = auto()           # # on a phone or remote control device. This key is typically found below the 9 key and to the right of the 0 key.
    # NumpadMemoryAdd = auto()      # M+ Add current entry to the value stored in memory.
    # NumpadMemoryClear = auto()    # MC Clear the value stored in memory.
    # NumpadMemoryRecall = auto()   # MR Replace the current entry with the value stored in memory.
    # NumpadMemoryStore = auto()    # MS Replace the value stored in memory with the current entry.
    # NumpadMemorySubtract = auto() # M- Subtract current entry from the value stored in memory.
    # NumpadParenLeft = auto()      # ( Found on the Microsoft Natural Keyboard.
    # NumpadParenRight = auto()     # ) Found on the Microsoft Natural Keyboard.
    # NumpadStar = auto()           # * on a phone or remote control device. This key is typically found below the 7 key and to the left of the 0 key. Use "NumpadMultiply" for the * key on numeric keypads.

    # ---------------------   Function Section   -----------------------------
    # https://w3c.github.io/uievents-code/#key-function-section
    # The function section runs along the top of the keyboard (above the alphanumeric
    # section) and contains the function keys and a few additional special keys
    # (for example, Esc and Print Screen). A function key is any of the keys labelled
    # F1 ... F12 that an application or operating system can associate with a
    # custom function or action.
    # ------------------------------------------------------------------------

    Escape = auto() 	    # Esc or ⎋
    F1 = auto() 	        # F1
    F2 = auto() 	        # F2
    F3 = auto() 	        # F3
    F4 = auto() 	        # F4
    F5 = auto() 	        # F5
    F6 = auto() 	        # F6
    F7 = auto() 	        # F7
    F8 = auto() 	        # F8
    F9 = auto() 	        # F9
    F10 = auto()            # F10
    F11 = auto()            # F11
    F12 = auto()            # F12
    PrintScreen = auto()    # PrtScr SysRq or Print Screen
    ScrollLock = auto() 	# Scroll Lock
    Pause = auto()          # Pause Break
    # Fn = auto() 	        # Fn This is typically a hardware key that does not generate a separate code. Most keyboards do not place this key in the function section, but it is included here to keep it with related keys.
    # FnLock = auto() 	    # FLock or FnLock. Function Lock key. Found on the Microsoft Natural Keyboard.

    # ---------------------   Media Keys   ----------------------------
    # https://w3c.github.io/uievents-code/#key-media
    # none of these are required to conform to the spec, and are omitted for now

    # ------------ Legacy, Non-Standard and Special Keys --------------
    # https://w3c.github.io/uievents-code/#key-legacy
    # none of these are required to conform to the spec, and are omitted for now

    def __str__(self) -> str:
        return scancode_to_string(self)

    @classmethod
    def from_string(cls, string: str) -> 'ScanCode':
        """Return the KeyCode associated with the given string.

        Returns ScanCode.UNIDENTIFIED if no match is found.
        """
        return scancode_from_string(string)




_EVENTCODE_TO_KEYCODE: Dict[int, KeyCode] = {}
_NATIVE_WINDOWS_VK_TO_KEYCODE: Dict[str, KeyCode] = {}


# build in a closure to prevent modification and declutter namespace
def _build_maps() -> Tuple[
    Callable[[KeyCode], str],
    Callable[[str], KeyCode],
    Callable[[KeyCode, OperatingSystem], str],
    Callable[[KeyCode, OperatingSystem], str],
    Callable[[ScanCode], str],
    Callable[[str], ScanCode],
]:
    class _KM(NamedTuple):
        scancode: ScanCode
        scanstr: str
        keycode: KeyCode
        keystr: str
        eventcode: int
        virtual_key: str

    _ = ''
    _MAPPINGS = [
        _KM(ScanCode.UNIDENTIFIED, 'None', KeyCode.UNKNOWN, 'unknown', 0, 'VK_UNKNOWN'),
        _KM(ScanCode.KeyA, 'KeyA', KeyCode.KeyA, 'A', 65, 'VK_A'),
        _KM(ScanCode.KeyB, 'KeyB', KeyCode.KeyB, 'B', 66, 'VK_B'),
        _KM(ScanCode.KeyC, 'KeyC', KeyCode.KeyC, 'C', 67, 'VK_C'),
        _KM(ScanCode.KeyD, 'KeyD', KeyCode.KeyD, 'D', 68, 'VK_D'),
        _KM(ScanCode.KeyE, 'KeyE', KeyCode.KeyE, 'E', 69, 'VK_E'),
        _KM(ScanCode.KeyF, 'KeyF', KeyCode.KeyF, 'F', 70, 'VK_F'),
        _KM(ScanCode.KeyG, 'KeyG', KeyCode.KeyG, 'G', 71, 'VK_G'),
        _KM(ScanCode.KeyH, 'KeyH', KeyCode.KeyH, 'H', 72, 'VK_H'),
        _KM(ScanCode.KeyI, 'KeyI', KeyCode.KeyI, 'I', 73, 'VK_I'),
        _KM(ScanCode.KeyJ, 'KeyJ', KeyCode.KeyJ, 'J', 74, 'VK_J'),
        _KM(ScanCode.KeyK, 'KeyK', KeyCode.KeyK, 'K', 75, 'VK_K'),
        _KM(ScanCode.KeyL, 'KeyL', KeyCode.KeyL, 'L', 76, 'VK_L'),
        _KM(ScanCode.KeyM, 'KeyM', KeyCode.KeyM, 'M', 77, 'VK_M'),
        _KM(ScanCode.KeyN, 'KeyN', KeyCode.KeyN, 'N', 78, 'VK_N'),
        _KM(ScanCode.KeyO, 'KeyO', KeyCode.KeyO, 'O', 79, 'VK_O'),
        _KM(ScanCode.KeyP, 'KeyP', KeyCode.KeyP, 'P', 80, 'VK_P'),
        _KM(ScanCode.KeyQ, 'KeyQ', KeyCode.KeyQ, 'Q', 81, 'VK_Q'),
        _KM(ScanCode.KeyR, 'KeyR', KeyCode.KeyR, 'R', 82, 'VK_R'),
        _KM(ScanCode.KeyS, 'KeyS', KeyCode.KeyS, 'S', 83, 'VK_S'),
        _KM(ScanCode.KeyT, 'KeyT', KeyCode.KeyT, 'T', 84, 'VK_T'),
        _KM(ScanCode.KeyU, 'KeyU', KeyCode.KeyU, 'U', 85, 'VK_U'),
        _KM(ScanCode.KeyV, 'KeyV', KeyCode.KeyV, 'V', 86, 'VK_V'),
        _KM(ScanCode.KeyW, 'KeyW', KeyCode.KeyW, 'W', 87, 'VK_W'),
        _KM(ScanCode.KeyX, 'KeyX', KeyCode.KeyX, 'X', 88, 'VK_X'),
        _KM(ScanCode.KeyY, 'KeyY', KeyCode.KeyY, 'Y', 89, 'VK_Y'),
        _KM(ScanCode.KeyZ, 'KeyZ', KeyCode.KeyZ, 'Z', 90, 'VK_Z'),
        _KM(ScanCode.Digit1, 'Digit1', KeyCode.Digit1, '1', 49, 'VK_1'),
        _KM(ScanCode.Digit2, 'Digit2', KeyCode.Digit2, '2', 50, 'VK_2'),
        _KM(ScanCode.Digit3, 'Digit3', KeyCode.Digit3, '3', 51, 'VK_3'),
        _KM(ScanCode.Digit4, 'Digit4', KeyCode.Digit4, '4', 52, 'VK_4'),
        _KM(ScanCode.Digit5, 'Digit5', KeyCode.Digit5, '5', 53, 'VK_5'),
        _KM(ScanCode.Digit6, 'Digit6', KeyCode.Digit6, '6', 54, 'VK_6'),
        _KM(ScanCode.Digit7, 'Digit7', KeyCode.Digit7, '7', 55, 'VK_7'),
        _KM(ScanCode.Digit8, 'Digit8', KeyCode.Digit8, '8', 56, 'VK_8'),
        _KM(ScanCode.Digit9, 'Digit9', KeyCode.Digit9, '9', 57, 'VK_9'),
        _KM(ScanCode.Digit0, 'Digit0', KeyCode.Digit0, '0', 48, 'VK_0'),
        _KM(ScanCode.Enter, 'Enter', KeyCode.Enter, 'Enter', 13, 'VK_RETURN'),
        _KM(ScanCode.Escape, 'Escape', KeyCode.Escape, 'Escape', 27, 'VK_ESCAPE'),
        _KM(ScanCode.Backspace, 'Backspace', KeyCode.Backspace, 'Backspace', 8, 'VK_BACK'),
        _KM(ScanCode.Tab, 'Tab', KeyCode.Tab, 'Tab', 9, 'VK_TAB'),
        _KM(ScanCode.Space, 'Space', KeyCode.Space, 'Space', 32, 'VK_SPACE'),
        _KM(ScanCode.Minus, 'Minus', KeyCode.Minus, '-', 189, 'VK_OEM_MINUS'),
        _KM(ScanCode.Equal, 'Equal', KeyCode.Equal, '=', 187, 'VK_OEM_PLUS'),
        _KM(ScanCode.BracketLeft, 'BracketLeft', KeyCode.BracketLeft, '[', 219, 'VK_OEM_4'),
        _KM(ScanCode.BracketRight, 'BracketRight', KeyCode.BracketRight, ']', 221, 'VK_OEM_6'),
        _KM(ScanCode.Backslash, 'Backslash', KeyCode.Backslash, '\\', 220, 'VK_OEM_5'),
        _KM(ScanCode.Semicolon, 'Semicolon', KeyCode.Semicolon, ';', 186, 'VK_OEM_1'),
        _KM(ScanCode.Quote, 'Quote', KeyCode.Quote, "'", 222, 'VK_OEM_7'),
        _KM(ScanCode.Backquote, 'Backquote', KeyCode.Backquote, '`', 192, 'VK_OEM_3'),
        _KM(ScanCode.Comma, 'Comma', KeyCode.Comma, ',', 188, 'VK_OEM_COMMA'),
        _KM(ScanCode.Period, 'Period', KeyCode.Period, '.', 190, 'VK_OEM_PERIOD'),
        _KM(ScanCode.Slash, 'Slash', KeyCode.Slash, '/', 191, 'VK_OEM_2'),
        _KM(ScanCode.CapsLock, 'CapsLock', KeyCode.CapsLock, 'CapsLock', 20, 'VK_CAPITAL'),
        _KM(ScanCode.F1, 'F1', KeyCode.F1, 'F1', 112, 'VK_F1'),
        _KM(ScanCode.F2, 'F2', KeyCode.F2, 'F2', 113, 'VK_F2'),
        _KM(ScanCode.F3, 'F3', KeyCode.F3, 'F3', 114, 'VK_F3'),
        _KM(ScanCode.F4, 'F4', KeyCode.F4, 'F4', 115, 'VK_F4'),
        _KM(ScanCode.F5, 'F5', KeyCode.F5, 'F5', 116, 'VK_F5'),
        _KM(ScanCode.F6, 'F6', KeyCode.F6, 'F6', 117, 'VK_F6'),
        _KM(ScanCode.F7, 'F7', KeyCode.F7, 'F7', 118, 'VK_F7'),
        _KM(ScanCode.F8, 'F8', KeyCode.F8, 'F8', 119, 'VK_F8'),
        _KM(ScanCode.F9, 'F9', KeyCode.F9, 'F9', 120, 'VK_F9'),
        _KM(ScanCode.F10, 'F10', KeyCode.F10, 'F10', 121, 'VK_F10'),
        _KM(ScanCode.F11, 'F11', KeyCode.F11, 'F11', 122, 'VK_F11'),
        _KM(ScanCode.F12, 'F12', KeyCode.F12, 'F12', 123, 'VK_F12'),
        _KM(ScanCode.PrintScreen, 'PrintScreen', KeyCode.PrintScreen, "PrintScreen", 42, "VK_PRINT"),
        _KM(ScanCode.ScrollLock, 'ScrollLock', KeyCode.ScrollLock, 'ScrollLock', 145, 'VK_SCROLL'),
        _KM(ScanCode.Pause, 'Pause', KeyCode.PauseBreak, 'PauseBreak', 19, 'VK_PAUSE'),
        _KM(ScanCode.Insert, 'Insert', KeyCode.Insert, 'Insert', 45, 'VK_INSERT'),
        _KM(ScanCode.Home, 'Home', KeyCode.Home, 'Home', 36, 'VK_HOME'),
        _KM(ScanCode.PageUp, 'PageUp', KeyCode.PageUp, 'PageUp', 33, 'VK_PRIOR'),
        _KM(ScanCode.Delete, 'Delete', KeyCode.Delete, 'Delete', 46, 'VK_DELETE'),
        _KM(ScanCode.End, 'End', KeyCode.End, 'End', 35, 'VK_END'),
        _KM(ScanCode.PageDown, 'PageDown', KeyCode.PageDown, 'PageDown', 34, 'VK_NEXT'),
        _KM(ScanCode.ArrowRight, 'ArrowRight', KeyCode.RightArrow, 'Right', 39, 'VK_RIGHT'),
        _KM(ScanCode.ArrowLeft, 'ArrowLeft', KeyCode.LeftArrow, 'Left', 37, 'VK_LEFT'),
        _KM(ScanCode.ArrowDown, 'ArrowDown', KeyCode.DownArrow, 'Down', 40, 'VK_DOWN'),
        _KM(ScanCode.ArrowUp, 'ArrowUp', KeyCode.UpArrow, 'Up', 38, 'VK_UP'),
        _KM(ScanCode.NumLock, 'NumLock', KeyCode.NumLock, 'NumLock', 144, 'VK_NUMLOCK'),
        _KM(ScanCode.NumpadDivide, 'NumpadDivide', KeyCode.NumpadDivide, 'NumPad_Divide', 111, 'VK_DIVIDE'),
        _KM(ScanCode.NumpadMultiply, 'NumpadMultiply', KeyCode.NumpadMultiply, 'NumPad_Multiply', 106, 'VK_MULTIPLY'),
        _KM(ScanCode.NumpadSubtract, 'NumpadSubtract', KeyCode.NumpadSubtract, 'NumPad_Subtract', 109, 'VK_SUBTRACT'),
        _KM(ScanCode.NumpadAdd, 'NumpadAdd', KeyCode.NumpadAdd, 'NumPad_Add', 107, 'VK_ADD'),
        _KM(ScanCode.NumpadEnter, 'NumpadEnter', KeyCode.Enter, _, 0, _),
        _KM(ScanCode.Numpad1, 'Numpad1', KeyCode.Numpad1, 'NumPad1', 97, 'VK_NUMPAD1'),
        _KM(ScanCode.Numpad2, 'Numpad2', KeyCode.Numpad2, 'NumPad2', 98, 'VK_NUMPAD2'),
        _KM(ScanCode.Numpad3, 'Numpad3', KeyCode.Numpad3, 'NumPad3', 99, 'VK_NUMPAD3'),
        _KM(ScanCode.Numpad4, 'Numpad4', KeyCode.Numpad4, 'NumPad4', 100, 'VK_NUMPAD4'),
        _KM(ScanCode.Numpad5, 'Numpad5', KeyCode.Numpad5, 'NumPad5', 101, 'VK_NUMPAD5'),
        _KM(ScanCode.Numpad6, 'Numpad6', KeyCode.Numpad6, 'NumPad6', 102, 'VK_NUMPAD6'),
        _KM(ScanCode.Numpad7, 'Numpad7', KeyCode.Numpad7, 'NumPad7', 103, 'VK_NUMPAD7'),
        _KM(ScanCode.Numpad8, 'Numpad8', KeyCode.Numpad8, 'NumPad8', 104, 'VK_NUMPAD8'),
        _KM(ScanCode.Numpad9, 'Numpad9', KeyCode.Numpad9, 'NumPad9', 105, 'VK_NUMPAD9'),
        _KM(ScanCode.Numpad0, 'Numpad0', KeyCode.Numpad0, 'NumPad0', 96, 'VK_NUMPAD0'),
        _KM(ScanCode.NumpadDecimal, 'NumpadDecimal', KeyCode.NumpadDecimal, 'NumPad_Decimal', 110, 'VK_DECIMAL'),
        _KM(ScanCode.IntlBackslash, 'IntlBackslash', KeyCode.IntlBackslash, 'OEM_102', 226, 'VK_OEM_102'),
        _KM(ScanCode.ContextMenu, 'ContextMenu', KeyCode.ContextMenu, 'ContextMenu', 93, _),
        _KM(ScanCode.NumpadEqual, 'NumpadEqual', KeyCode.UNKNOWN, _, 0, _),
        _KM(ScanCode.Help, 'Help', KeyCode.UNKNOWN, _, 0, _),
        _KM(ScanCode.IntlRo, 'IntlRo', KeyCode.UNKNOWN, _, 193, 'VK_ABNT_C1'),
        _KM(ScanCode.KanaMode, 'KanaMode', KeyCode.UNKNOWN, _, 0, _),
        _KM(ScanCode.IntlYen, 'IntlYen', KeyCode.UNKNOWN, _, 0, _),
        _KM(ScanCode.Convert, 'Convert', KeyCode.UNKNOWN, _, 0, _),
        _KM(ScanCode.NonConvert, 'NonConvert', KeyCode.UNKNOWN, _, 0, _),
        _KM(ScanCode.UNIDENTIFIED, _, KeyCode.Ctrl, 'Ctrl', 17, 'VK_CONTROL'),
        _KM(ScanCode.UNIDENTIFIED, _, KeyCode.Shift, 'Shift', 16, 'VK_SHIFT'),
        _KM(ScanCode.UNIDENTIFIED, _, KeyCode.Alt, 'Alt', 18, 'VK_MENU'),
        _KM(ScanCode.UNIDENTIFIED, _, KeyCode.Meta, 'Meta', 0, 'VK_COMMAND'),
        _KM(ScanCode.ControlLeft, 'ControlLeft', KeyCode.Ctrl, _, 0, 'VK_LCONTROL'),
        _KM(ScanCode.ShiftLeft, 'ShiftLeft', KeyCode.Shift, _, 0, 'VK_LSHIFT'),
        _KM(ScanCode.AltLeft, 'AltLeft', KeyCode.Alt, _, 0, 'VK_LMENU'),
        _KM(ScanCode.MetaLeft, 'MetaLeft', KeyCode.Meta, _, 0, 'VK_LWIN'),
        _KM(ScanCode.ControlRight, 'ControlRight', KeyCode.Ctrl, _, 0, 'VK_RCONTROL'),
        _KM(ScanCode.ShiftRight, 'ShiftRight', KeyCode.Shift, _, 0, 'VK_RSHIFT'),
        _KM(ScanCode.AltRight, 'AltRight', KeyCode.Alt, _, 0, 'VK_RMENU'),
        _KM(ScanCode.MetaRight, 'MetaRight', KeyCode.Meta, _, 0, 'VK_RWIN'),
    ]

    SCANCODE_TO_STRING: Dict[ScanCode, str] = {}
    SCANCODE_FROM_LOWERCASE_STRING: Dict[str, ScanCode] = {}

    KEYCODE_TO_STRING: Dict[KeyCode, str] = {}
    KEYCODE_FROM_LOWERCASE_STRING: Dict[str, KeyCode] = {
        # two special cases for assigning os-specific strings to the meta key
        'win': KeyCode.Meta,
        'cmd': KeyCode.Meta,
    }

    # key symbols on all platforms
    KEY_SYMBOLS: dict[KeyCode, str] = {
        KeyCode.Shift: "⇧",
        KeyCode.LeftArrow: "←",
        KeyCode.RightArrow: "→",
        KeyCode.UpArrow: "↑",
        KeyCode.DownArrow: "↓",
        KeyCode.Backspace: "⌫",
        KeyCode.Delete: "⌦",
        KeyCode.Tab: "⇥",
        KeyCode.Escape: "⎋",
        KeyCode.Enter: "↵",
        KeyCode.Space: "␣",
        KeyCode.CapsLock: "⇪",
    }
    # key symbols mappings per platform
    OS_KEY_SYMBOLS: dict[OperatingSystem, dict[KeyCode, str]] = {
        OperatingSystem.WINDOWS: {**KEY_SYMBOLS, KeyCode.Meta: "⊞"},
        OperatingSystem.LINUX: {**KEY_SYMBOLS, KeyCode.Meta: "Super"},
        OperatingSystem.MACOS: {
            **KEY_SYMBOLS,
            KeyCode.Ctrl: "⌃",
            KeyCode.Alt: "⌥",
            KeyCode.Meta: "⌘",
        },
    }

    # key names mappings per platform
    OS_KEY_NAMES: dict[OperatingSystem, dict[KeyCode, str]] = {
        OperatingSystem.WINDOWS: {KeyCode.Meta: "Win"},
        OperatingSystem.LINUX: {KeyCode.Meta: "Super"},
        OperatingSystem.MACOS: {
            KeyCode.Ctrl: "Control",
            KeyCode.Alt: "Option",
            KeyCode.Meta: "Cmd",
        },
    }

    seen_scancodes: Set[ScanCode] = set()
    seen_keycodes: Set[KeyCode] = set()
    for i, km in enumerate(_MAPPINGS):
        if km.scancode not in seen_scancodes:
            seen_scancodes.add(km.scancode)
            SCANCODE_TO_STRING[km.scancode] = km.scanstr
            SCANCODE_FROM_LOWERCASE_STRING[km.scanstr.lower()] = km.scancode
        if km.keycode not in seen_keycodes:
            seen_keycodes.add(km.keycode)
            if not km.keystr:  # pragma: no cover
                raise ValueError(
                    f"String representation missing for key code {km.keycode!r} "
                    f"around scan code {km.scancode!r} at line {i + 1}"
                )
            KEYCODE_TO_STRING[km.keycode] = km.keystr
            KEYCODE_FROM_LOWERCASE_STRING[km.keystr.lower()] = km.keycode
        if km.eventcode:
            _EVENTCODE_TO_KEYCODE[km.eventcode] = km.keycode
        if km.virtual_key:
            _NATIVE_WINDOWS_VK_TO_KEYCODE[km.virtual_key] = km.keycode

    def _keycode_to_string(keycode: KeyCode) -> str:
        """Return the string representation of a KeyCode."""
        # sourcery skip
        return KEYCODE_TO_STRING.get(keycode, "")

    def _keycode_from_string(keystr: str) -> KeyCode:
        """Return KeyCode for a given string."""
        # sourcery skip
        return KEYCODE_FROM_LOWERCASE_STRING.get(str(keystr).lower(), KeyCode.UNKNOWN)

    def _keycode_to_os_symbol(keycode: KeyCode, os: OperatingSystem) -> str:
        """Return key symbol for an OS for a given KeyCode."""
        if keycode in (symbols := OS_KEY_SYMBOLS.get(os, {})):
            return symbols[keycode]
        return str(keycode)

    def _keycode_to_os_name(keycode: KeyCode, os: OperatingSystem) -> str:
        """Return key name for an OS for a given KeyCode."""
        if keycode in (names := OS_KEY_NAMES.get(os, {})):
            return names[keycode]
        return str(keycode)

    def _scancode_to_string(scancode: ScanCode) -> str:
        """Return the string representation of a ScanCode."""
        # sourcery skip
        return SCANCODE_TO_STRING.get(scancode, "")

    def _scancode_from_string(scanstr: str) -> ScanCode:
        """Return ScanCode for a given string."""
        # sourcery skip
        return SCANCODE_FROM_LOWERCASE_STRING.get(
            str(scanstr).lower(), ScanCode.UNIDENTIFIED
        )

    return (
        _keycode_to_string,
        _keycode_from_string,
        _keycode_to_os_symbol,
        _keycode_to_os_name,
        _scancode_to_string,
        _scancode_from_string,
    )


(
    keycode_to_string,
    keycode_from_string,
    keycode_to_os_symbol,
    keycode_to_os_name,
    scancode_to_string,
    scancode_from_string,
) = _build_maps()


# fmt: on

# Keys with modifiers are expressed
# with a 16-bit binary encoding
#
#    1111 11
#    5432 1098 7654 3210
#    ---- CSAW KKKK KKKK
#  C = bit 11   -> ctrlCmd flag
#  S = bit 10   -> shift flag
#  A = bit 9    -> alt flag
#  W = bit 8    -> winCtrl flag
#  K = bits 0-7 -> key code


class KeyMod(IntFlag):
    """A Flag indicating keyboard modifiers."""

    NONE = 0
    CtrlCmd = 1 << 11  # command on a mac, control on windows
    Shift = 1 << 10  # shift key
    Alt = 1 << 9  # alt option
    WinCtrl = 1 << 8  # meta key on windows, ctrl key on mac

    @overload  # type: ignore
    def __or__(self, other: "KeyMod") -> "KeyMod": ...

    @overload
    def __or__(self, other: KeyCode) -> "KeyCombo": ...

    @overload
    def __or__(self, other: int) -> int: ...

    def __or__(
        self, other: Union["KeyMod", KeyCode, int]
    ) -> Union["KeyMod", "KeyCombo", int]:
        if isinstance(other, self.__class__):
            return self.__class__(self._value_ | other._value_)
        if isinstance(other, KeyCode):
            return KeyCombo(self, other)
        return NotImplemented  # pragma: no cover


class KeyCombo(int):
    """KeyCombo is an integer combination of one or more.

    [`KeyMod`][app_model.types.KeyMod] and [`KeyCode`][app_model.types.KeyCode].
    """

    def __new__(
        cls: Type["KeyCombo"], modifiers: KeyMod, key: KeyCode = KeyCode.UNKNOWN
    ) -> "KeyCombo":
        return super().__new__(cls, int(modifiers) | int(key))

    def __init__(self, modifiers: KeyMod, key: KeyCode = KeyCode.UNKNOWN):
        self._modifiers = modifiers
        self._key = key

    def __repr__(self) -> str:
        name = self.__class__.__name__
        mods_repr = repr(self._modifiers).split(":", 1)[0].split(".", 1)[1]
        return f"<{name}.{mods_repr}|{self._key.name}: {int(self)}>"


class KeyChord(int):
    """KeyChord is an integer combination of two key combos.

    It could be two [`KeyCombo`][app_model.types.KeyCombo]
    [`KeyCode`][app_model.types.KeyCode], or [int][].

    Parameters
    ----------
    first_part : KeyCombo | int
        The first part of the chord.
    second_part : KeyCombo | int
        The second part of the chord.
    """

    def __new__(cls: Type["KeyChord"], first_part: int, second_part: int) -> "KeyChord":
        # shift the second part 16 bits to the left
        chord_part = (second_part & 0x0000FFFF) << 16
        # then combine then to make the full chord
        return super().__new__(cls, first_part | chord_part)

    def __init__(self, first_part: int, second_part: int):
        self._first_part = first_part
        self._second_part = second_part

    def __repr__(self) -> str:
        return f"KeyChord({self._first_part!r}, {self._second_part!r})"
