from typing import NewType, Optional, TypedDict, Union

from pydantic import Field

from .. import expressions
from ._base import _StrictModel
from ._constants import OperatingSystem

KeyCodeStr = NewType("KeyCodeStr", str)
KeyEncoding = Union[int, str]

_OS = OperatingSystem.current()
_WIN = _OS.is_windows
_MAC = _OS.is_mac
_LINUX = _OS.is_linux


class KeyBindingRule(_StrictModel):
    """Data representing a keybinding and when it should be active.

    This model lacks a corresponding command. That gets linked up elsewhere,
    such as below in `Action`.
    """

    primary: Optional[KeyEncoding] = Field(
        None, description="(Optional) Key combo, (e.g. Ctrl+O)."
    )
    win: Optional[KeyEncoding] = Field(
        None, description="(Optional) Windows specific key combo."
    )
    linux: Optional[KeyEncoding] = Field(
        None, description="(Optional) Linux specific key combo."
    )
    mac: Optional[KeyEncoding] = Field(
        None, description="(Optional) MacOS specific key combo."
    )
    when: Optional[expressions.Expr] = Field(
        None,
        description="(Optional) Condition when the keybingding is active.",
    )
    weight: int = Field(
        0,
        description="Internal weight used to sort keybindings. "
        "This is not part of the plugin schema",
    )

    def _bind_to_current_platform(self) -> Optional[KeyEncoding]:
        if _WIN and self.win:
            return self.win
        if _MAC and self.mac:
            return self.mac
        if _LINUX and self.linux:
            return self.linux
        return self.primary


class KeyBindingRuleDict(TypedDict, total=False):
    """Typed dict for KeyBindingRule kwargs."""

    primary: Optional[KeyCodeStr]
    win: Optional[KeyCodeStr]
    linux: Optional[KeyCodeStr]
    mac: Optional[KeyCodeStr]
    weight: int
    when: Optional[expressions.Expr]


KeyBindingRuleOrDict = Union[KeyBindingRule, KeyBindingRuleDict]
