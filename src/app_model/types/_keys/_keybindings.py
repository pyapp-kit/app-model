import re
from functools import lru_cache
from typing import (
    Any,
    Callable,
    Dict,
    Generator,
    List,
    Optional,
    Sequence,
    Tuple,
    Type,
    Union,
)

from pydantic import BaseModel

from .._constants import OperatingSystem
from ._key_codes import KeyChord, KeyCode, KeyMod

_re_ctrl = re.compile(r"ctrl[\+|\-]")
_re_shift = re.compile(r"shift[\+|\-]")
_re_alt = re.compile(r"alt[\+|\-]")
_re_meta = re.compile(r"meta[\+|\-]")
_re_win = re.compile(r"win[\+|\-]")
_re_cmd = re.compile(r"cmd[\+|\-]")


class SimpleKeyBinding(BaseModel):
    """Represent a simple combination modifier(s) and a key, e.g. Ctrl+A."""

    ctrl: bool = False
    shift: bool = False
    alt: bool = False
    meta: bool = False
    key: Optional[KeyCode] = None

    # def hash_code(self) -> str:
    # used by vscode for caching during keybinding resolution

    def is_modifier_key(self) -> bool:
        """Return true if this is a modifier key."""
        return self.key in (
            KeyCode.Alt,
            KeyCode.Shift,
            KeyCode.Ctrl,
            KeyCode.Meta,
            KeyCode.UNKNOWN,
        )

    def __str__(self) -> str:
        out = ""
        if self.ctrl:
            out += "Ctrl+"
        if self.shift:
            out += "Shift+"
        if self.alt:
            out += "Alt+"
        if self.meta:
            out += "Meta+"
        if self.key:
            out += str(self.key)
        return out

    def __eq__(self, other: Any) -> bool:
        # sourcery skip: remove-unnecessary-cast
        if not isinstance(other, SimpleKeyBinding):
            try:
                other = SimpleKeyBinding.validate(other)
            except TypeError:
                return NotImplemented
        return bool(
            self.ctrl == other.ctrl
            and self.shift == other.shift
            and self.alt == other.alt
            and self.meta == other.meta
            and self.key == other.key
        )

    @classmethod
    def from_str(cls, key_str: str) -> "SimpleKeyBinding":
        """Parse a string into a SimpleKeyBinding."""
        mods, remainder = _parse_modifiers(key_str.strip())
        key = KeyCode.from_string(remainder)
        return cls(**mods, key=key)

    @classmethod
    def from_int(
        cls, key_int: int, os: Optional[OperatingSystem] = None
    ) -> "SimpleKeyBinding":
        """Create a SimpleKeyBinding from an integer."""
        ctrl_cmd = bool(key_int & KeyMod.CtrlCmd)
        win_ctrl = bool(key_int & KeyMod.WinCtrl)
        shift = bool(key_int & KeyMod.Shift)
        alt = bool(key_int & KeyMod.Alt)

        os = OperatingSystem.current() if os is None else os
        ctrl = win_ctrl if os.is_mac else ctrl_cmd
        meta = ctrl_cmd if os.is_mac else win_ctrl
        key = key_int & 0x000000FF  # keycode mask

        return cls(ctrl=ctrl, shift=shift, alt=alt, meta=meta, key=key)

    def __int__(self) -> int:
        return int(self.to_int())

    def __hash__(self) -> int:
        return hash((self.ctrl, self.shift, self.alt, self.meta, self.key))

    def to_int(self, os: Optional[OperatingSystem] = None) -> int:
        """Convert this SimpleKeyBinding to an integer representation."""
        os = OperatingSystem.current() if os is None else os
        mods: KeyMod = KeyMod.NONE
        if self.ctrl:
            mods |= KeyMod.WinCtrl if os.is_mac else KeyMod.CtrlCmd
        if self.shift:
            mods |= KeyMod.Shift
        if self.alt:
            mods |= KeyMod.Alt
        if self.meta:
            mods |= KeyMod.CtrlCmd if os.is_mac else KeyMod.WinCtrl
        return mods | (self.key or 0)

    @classmethod
    def __get_validators__(cls) -> Generator[Callable[..., Any], None, None]:
        yield cls.validate  # pragma: no cover

    @classmethod
    def validate(cls, v: Any) -> "SimpleKeyBinding":
        """Validate a SimpleKeyBinding."""
        if isinstance(v, SimpleKeyBinding):
            return v
        if isinstance(v, str):
            return cls.from_str(v)
        if isinstance(v, int):
            return cls.from_int(v)
        return super().validate(v)


class KeyBinding(str):
    """KeyBinding.  May be a multi-part "Chord" (e.g. 'Ctrl+K Ctrl+C').

    This is the primary representation of a fully resolved keybinding. For consistency
    in the downstream API, it should  be preferred to :class:`SimplyKeyBinding`, even
    when there is only a single part in the keybinding (i.e. when it is not a chord.)

    Chords (two separate keypress actions) are expressed as a string by separating
    the two keypress codes with a space. For example, 'Ctrl+K Ctrl+C'.
    """

    def __new__(
        cls: Type["KeyBinding"],
        parts: Union[str, Sequence[Union[str, int, SimpleKeyBinding]]],
    ) -> "KeyBinding":
        """Normalize a keybinding."""
        if isinstance(parts, str):
            parts = cls.str_to_parts(parts)

        if not parts:
            raise ValueError("invalid keybinding")

        return super().__new__(cls, cls.parts_to_str(parts))

    @staticmethod
    def parts_to_str(parts: Sequence[Union[str, int, SimpleKeyBinding]]) -> str:
        """How parts are converted to a string.

        Subclass and override this to change string representation.
        """
        return " ".join(str(SimpleKeyBinding.validate(part)) for part in parts)

    @staticmethod
    @lru_cache
    def str_to_parts(s: str) -> List[SimpleKeyBinding]:
        """How the string representation is converted to parts.

        Subclass and override this to change string representation.
        It is recommended to cache this function.
        """
        parts = []
        for part in s.split():
            kb = SimpleKeyBinding.from_str(part)
            if kb.key == KeyCode.UNKNOWN:
                raise ValueError(f"invalid part {part}")
            parts.append(kb)

        return parts

    @property
    def parts(self) -> List[SimpleKeyBinding]:
        """Key combinations that make up the overall key chord."""
        return self.str_to_parts(self)

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, KeyBinding):
            try:
                other = KeyBinding.validate(other)
            except Exception:  # pragma: no cover
                return NotImplemented
        return super().__eq__(other)

    def __len__(self) -> int:
        return len(self.parts)

    @property
    def part0(self) -> SimpleKeyBinding:
        """Return the first part of this keybinding.

        All keybindings have at least one part.
        """
        return self.parts[0]

    @classmethod
    def from_str(cls, key_str: str) -> "KeyBinding":
        """Parse a string into a SimpleKeyBinding."""
        return cls(key_str)

    @classmethod
    def from_int(
        cls, key_int: int, os: Optional[OperatingSystem] = None
    ) -> "KeyBinding":
        """Create a KeyBinding from an integer."""
        # a multi keybinding is represented as an integer
        # with the first_part in the lowest 16 bits,
        # the second_part in the next 16 bits, etc.
        first_part = key_int & 0x0000FFFF
        chord_part = (key_int & 0xFFFF0000) >> 16
        if chord_part != 0:
            return cls(
                parts=[
                    SimpleKeyBinding.from_int(first_part, os),
                    SimpleKeyBinding.from_int(chord_part, os),
                ]
            )
        return cls(parts=[SimpleKeyBinding.from_int(first_part, os)])

    def to_int(self, os: Optional[OperatingSystem] = None) -> int:
        """Convert this SimpleKeyBinding to an integer representation."""
        if len(self.parts) > 2:  # pragma: no cover
            raise NotImplementedError(
                "Cannot represent chords with more than 2 parts as int"
            )
        os = OperatingSystem.current() if os is None else os
        parts = [part.to_int(os) for part in self.parts]
        if len(parts) == 2:
            return KeyChord(*parts)
        return parts[0]

    def __int__(self) -> int:
        return int(self.to_int())

    def __hash__(self) -> int:
        return super().__hash__()

    @classmethod
    def __get_validators__(cls) -> Generator[Callable[..., Any], None, None]:
        yield cls.validate  # pragma: no cover

    @classmethod
    def validate(cls, v: Any) -> "KeyBinding":
        """Validate a SimpleKeyBinding."""
        if isinstance(v, KeyBinding):
            return v
        if isinstance(v, SimpleKeyBinding):
            return cls(parts=[v])
        if isinstance(v, int):
            return cls.from_int(v)
        if isinstance(v, str):
            return cls.from_str(v)
        raise TypeError("invalid keybinding")  # pragma: no cover


def _parse_modifiers(input: str) -> Tuple[Dict[str, bool], str]:
    """Parse modifiers from a string (case insensitive).

    modifiers must start at the beginning of the string, and be separated by
    "+" or "-".  e.g. "ctrl+shift+alt+K" or "Ctrl-Cmd-K"
    """
    remainder = input.lower()

    ctrl = False
    shift = False
    alt = False
    meta = False

    while True:
        saw_modifier = False
        if _re_ctrl.match(remainder):
            remainder = remainder[5:]
            ctrl = True
            saw_modifier = True
        if _re_shift.match(remainder):
            remainder = remainder[6:]
            shift = True
            saw_modifier = True
        if _re_alt.match(remainder):
            remainder = remainder[4:]
            alt = True
            saw_modifier = True
        if _re_meta.match(remainder):
            remainder = remainder[5:]
            meta = True
            saw_modifier = True
        if _re_win.match(remainder):
            remainder = remainder[4:]
            meta = True
            saw_modifier = True
        if _re_cmd.match(remainder):
            remainder = remainder[4:]
            meta = True
            saw_modifier = True
        if not saw_modifier:
            break

    return {"ctrl": ctrl, "shift": shift, "alt": alt, "meta": meta}, remainder
