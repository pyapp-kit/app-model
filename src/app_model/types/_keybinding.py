import os
import sys
from typing import NewType, Optional, TypedDict, Union

from pydantic import Field

from .. import expressions
from ._base import _StrictModel

WINDOWS = os.name == "nt"
MACOS = sys.platform == "darwin"
LINUX = sys.platform.startswith("linux")

KeyCodeStr = NewType("KeyCodeStr", str)


class KeybindingRule(_StrictModel):
    """Data representing a keybinding and when it should be active.

    This model lacks a corresponding command. That gets linked up elsewhere,
    such as below in `Action`.
    """

    primary: Optional[KeyCodeStr] = Field(
        None, description="(Optional) Key combo, (e.g. Ctrl+O)."
    )
    win: Optional[KeyCodeStr] = Field(
        None, description="(Optional) Windows specific key combo."
    )
    linux: Optional[KeyCodeStr] = Field(
        None, description="(Optional) Linux specific key combo."
    )
    mac: Optional[KeyCodeStr] = Field(
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

    def _bind_to_current_platform(self) -> Optional[KeyCodeStr]:
        if WINDOWS and self.win:
            return self.win
        if MACOS and self.mac:
            return self.mac
        if LINUX and self.linux:
            return self.linux
        return self.primary


class KeybindingRuleDict(TypedDict, total=False):
    """Typed dict for KeybindingRule kwargs."""

    primary: Optional[KeyCodeStr]
    win: Optional[KeyCodeStr]
    linux: Optional[KeyCodeStr]
    mac: Optional[KeyCodeStr]
    weight: int
    when: Optional[expressions.Expr]


KeybindingRuleOrDict = Union[KeybindingRule, KeybindingRuleDict]
