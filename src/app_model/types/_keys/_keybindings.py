import re
from typing import TYPE_CHECKING, Any, Callable, Dict, Generator, List, Optional, Tuple

from pydantic_compat import PYDANTIC2, BaseModel, Field, model_validator

from app_model.types._constants import OperatingSystem

from ._key_codes import KeyChord, KeyCode, KeyMod

if TYPE_CHECKING:
    from pydantic.annotated_handlers import GetCoreSchemaHandler
    from pydantic_core import core_schema


class SimpleKeyBinding(BaseModel):
    """Represent a simple combination modifier(s) and a key, e.g. Ctrl+A."""

    ctrl: bool = Field(False, description='Whether the "Ctrl" modifier is active.')
    shift: bool = Field(False, description='Whether the "Shift" modifier is active.')
    alt: bool = Field(False, description='Whether the "Alt" modifier is active.')
    meta: bool = Field(False, description='Whether the "Meta" modifier is active.')
    key: Optional[KeyCode] = Field(
        None, description="The key that is pressed (e.g. `KeyCode.A`)"
    )

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
        """Get a normalized string representation (constant to all OSes) of this SimpleKeyBinding."""
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
                if (other := SimpleKeyBinding._parse_input(other)) is None:
                    return NotImplemented
            except TypeError:  # pragma: no cover  # can happen with pydantic v2
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

    def _mods2keycodes(self) -> List[KeyCode]:
        """Create KeyCode instances list of modifiers from this SimpleKeyBinding."""
        mods = []
        if self.ctrl:
            mods.append(KeyCode.Ctrl)
        if self.shift:
            mods.append(KeyCode.Shift)
        if self.alt:
            mods.append(KeyCode.Alt)
        if self.meta:
            mods.append(KeyCode.Meta)
        return mods

    def to_text(
        self,
        os: Optional[OperatingSystem] = None,
        use_symbols: bool = False,
        joinchar: str = "+",
    ) -> str:
        """Get a user-facing string representation of this SimpleKeyBinding.

        Optionally, the string representation can be constructed with symbols
        like ↵ for Enter or OS specific ones like ⌘ for Meta on MacOS. If no symbols
        should be used, the string representation will use the OS specific names
        for the keys like `Cmd` for Meta or `Option` for Ctrl on MacOS.

        Also, a join character can be defined. By default `+` is used.
        """
        os = OperatingSystem.current() if os is None else os
        keybinding_elements = [*self._mods2keycodes()]
        if self.key:
            keybinding_elements.append(self.key)

        return joinchar.join(
            kbe.os_symbol(os=os) if use_symbols else kbe.os_name(os=os)
            for kbe in keybinding_elements
        )

    @classmethod
    def _parse_input(cls, v: Any) -> "SimpleKeyBinding":
        if isinstance(v, SimpleKeyBinding):
            return v
        if isinstance(v, str):
            return cls.from_str(v)
        if isinstance(v, int):
            return cls.from_int(v)
        raise TypeError(f"invalid type: {type(v)}")

    @model_validator(mode="after")  # type: ignore
    @classmethod
    def _model_val(cls, instance: "SimpleKeyBinding") -> "SimpleKeyBinding":
        return cls._parse_input(instance)


MIN1 = {"min_length": 1} if PYDANTIC2 else {"min_items": 1}


class KeyBinding:
    """KeyBinding.  May be a multi-part "Chord" (e.g. 'Ctrl+K Ctrl+C').

    This is the primary representation of a fully resolved keybinding. For consistency
    in the downstream API, it should be preferred to
    [`SimpleKeyBinding`][app_model.types.SimpleKeyBinding], even
    when there is only a single part in the keybinding (i.e. when it is not a chord.)

    Chords (two separate keypress actions) are expressed as a string by separating
    the two keypress codes with a space. For example, 'Ctrl+K Ctrl+C'.

    Parameters
    ----------
    parts : List[SimpleKeyBinding]
        The parts of the keybinding.  There must be at least one part.
    """

    parts: List[SimpleKeyBinding] = Field(..., **MIN1)  # type: ignore

    def __init__(self, *, parts: List[SimpleKeyBinding]):
        self.parts = parts

    def __str__(self) -> str:
        """Get a normalized string representation (constant to all OSes) of this KeyBinding."""
        return " ".join(str(part) for part in self.parts)

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} at {hex(id(self))}: {self}>"

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, KeyBinding):
            return self.parts == other.parts
        return NotImplemented

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
        parts = [SimpleKeyBinding.from_str(part) for part in key_str.split()]
        return cls(parts=parts)

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
        """Convert this KeyBinding to an integer representation."""
        if len(self.parts) > 2:  # pragma: no cover
            raise NotImplementedError(
                "Cannot represent chords with more than 2 parts as int"
            )
        os = OperatingSystem.current() if os is None else os
        parts = [part.to_int(os) for part in self.parts]
        if len(parts) == 2:
            return KeyChord(*parts)
        return parts[0]

    def to_text(
        self,
        os: Optional[OperatingSystem] = None,
        use_symbols: bool = False,
        joinchar: str = "+",
    ) -> str:
        """Get a text representation of this KeyBinding.

        Optionally, the string representation can be constructed with symbols
        like ↵ for Enter or OS specific ones like ⌘ for Meta on MacOS. If no symbols
        should be used, the string representation will use the OS specific names
        for the keys like `Cmd` for Meta or `Option` for Ctrl on MacOS.

        Also, a join character can be defined. By default `+` is used.
        """
        return " ".join(
            part.to_text(os=os, use_symbols=use_symbols, joinchar=joinchar)
            for part in self.parts
        )

    def __int__(self) -> int:
        return int(self.to_int())

    def __hash__(self) -> int:
        return hash(tuple(self.parts))

    @classmethod
    def __get_validators__(cls) -> Generator[Callable[..., Any], None, None]:
        yield cls.validate  # pragma: no cover

    @classmethod
    def __get_pydantic_core_schema__(
        cls, source: type, handler: "GetCoreSchemaHandler"
    ) -> "core_schema.CoreSchema":
        from pydantic_core import core_schema

        return core_schema.no_info_plain_validator_function(
            cls.validate, serialization=core_schema.to_string_ser_schema()
        )

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


_re_ctrl = re.compile(r"(ctrl|control|ctl|⌃|\^)[\+|\-]")
_re_shift = re.compile(r"(shift|⇧)[\+|\-]")
_re_alt = re.compile(r"(alt|opt|option|⌥)[\+|\-]")
_re_meta = re.compile(r"(meta|super|win|windows|⊞|cmd|command|⌘)[\+|\-]")


def _parse_modifiers(input: str) -> Tuple[Dict[str, bool], str]:
    """Parse modifiers from a string (case insensitive).

    modifiers must start at the beginning of the string, and be separated by
    "+" or "-".  e.g. "ctrl+shift+alt+K" or "Ctrl-Cmd-K"
    """
    remainder = input.lower()

    patterns = {"ctrl": _re_ctrl, "shift": _re_shift, "alt": _re_alt, "meta": _re_meta}
    mods = dict.fromkeys(patterns, False)
    while True:
        saw_modifier = False
        for key, ptrn in patterns.items():
            if m := ptrn.match(remainder):
                remainder = remainder[m.span()[1] :]
                mods[key] = True
                saw_modifier = True
                break
        if not saw_modifier:
            break

    return mods, remainder
