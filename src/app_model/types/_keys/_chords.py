import re
from typing import Any, Callable, Dict, Generator, List, Optional, Tuple, cast

from pydantic import BaseModel, Field

from .._constants import OperatingSystem
from ._key_codes import KeyCode, KeyMod

_re_ctrl = re.compile(r"ctrl[\+|\-]")
_re_shift = re.compile(r"shift[\+|\-]")
_re_alt = re.compile(r"alt[\+|\-]")
_re_meta = re.compile(r"meta[\+|\-]")
_re_win = re.compile(r"win[\+|\-]")
_re_cmd = re.compile(r"cmd[\+|\-]")


class SimpleKeyBinding(BaseModel):
    """Represent a simple key binding: Combination of key and modifier(s)."""

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
            KeyCode.UNKOWN,
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
        if not isinstance(other, ChordKeyBinding):
            try:
                other = ChordKeyBinding.validate(other)
            except Exception:
                return NotImplemented
        return cast(bool, super().__eq__(other))

    @classmethod
    def parse_str(cls, key_str: str) -> "SimpleKeyBinding":
        """Parse a string into a SimpleKeyBinding."""
        mods, remainder = _parse_modifiers(key_str.strip())
        key = KeyCode.from_string(remainder)
        return cls(**mods, key=key)

    @classmethod
    def parse_int(
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

    @classmethod
    def __get_validators__(cls) -> Generator[Callable[..., Any], None, None]:
        yield cls.validate

    @classmethod
    def validate(cls, v: Any) -> "SimpleKeyBinding":
        """Validate a SimpleKeyBinding."""
        if isinstance(v, SimpleKeyBinding):
            return v
        if isinstance(v, str):
            return cls.parse_str(v)
        if isinstance(v, int):
            return cls.parse_int(v)
        if isinstance(v, dict):
            return cls(**v)
        raise TypeError(f"KeyBinding must be a string or a dict, not {type(v)}")


class ChordKeyBinding(BaseModel):
    """Multi-part key binding "Chord".

    Chords (two separate keypress actions) are expressed as a string by separating
    the two keypress codes with a space. For example, 'Ctrl+K Ctrl+C'.
    """

    parts: List[SimpleKeyBinding] = Field(..., min_items=1)

    def __str__(self) -> str:
        return " ".join(str(part) for part in self.parts)

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, ChordKeyBinding):
            try:
                other = ChordKeyBinding.validate(other)
            except Exception:
                return NotImplemented
        return cast(bool, super().__eq__(other))

    @classmethod
    def parse_str(cls, key_str: str) -> "ChordKeyBinding":
        """Parse a string into a SimpleKeyBinding."""
        parts = [SimpleKeyBinding.parse_str(part) for part in key_str.split()]
        return cls(parts=parts)

    @classmethod
    def parse_int(
        cls, key_int: int, os: Optional[OperatingSystem] = None
    ) -> "ChordKeyBinding":
        """Create a ChordKeyBinding from an integer."""
        first_part = key_int & 0x0000FFFF
        chord_part = key_int & 0xFFFF0000
        if chord_part != 0:
            return cls(
                parts=[
                    SimpleKeyBinding.parse_int(first_part, os),
                    SimpleKeyBinding.parse_int(chord_part, os),
                ]
            )
        return cls(parts=[SimpleKeyBinding.parse_int(first_part, os)])

    @classmethod
    def __get_validators__(cls) -> Generator[Callable[..., Any], None, None]:
        yield cls.validate

    @classmethod
    def validate(cls, v: Any) -> "ChordKeyBinding":
        """Validate a SimpleKeyBinding."""
        if isinstance(v, ChordKeyBinding):
            return v
        if isinstance(v, int):
            return cls.parse_int(v)
        if isinstance(v, str):
            return cls.parse_str(v)
        if isinstance(v, dict):
            return cls(**v)
        raise TypeError(f"ChordKeyBinding must be a string or a dict, not {type(v)}")


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
