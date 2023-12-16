from typing import Any, Callable, Optional, Type, TypedDict, TypeVar, Union

from pydantic_compat import PYDANTIC2, Field, model_validator

from app_model import expressions

from ._base import _BaseModel
from ._constants import OperatingSystem
from ._keys import StandardKeyBinding

KeyEncoding = Union[int, str]
M = TypeVar("M")

_OS = OperatingSystem.current()
_WIN = _OS.is_windows
_MAC = _OS.is_mac
_LINUX = _OS.is_linux


class KeyBindingRule(_BaseModel):
    """Data representing a keybinding and when it should be active.

    This model lacks a corresponding command. That gets linked up elsewhere,
    such as below in `Action`.

    Values can be expressed as either a string (e.g. `"Ctrl+O"`) or an integer, using
    combinations of [`KeyMod`][app_model.types.KeyMod] and
    [`KeyCode`][app_model.types.KeyCode], (e.g. `KeyMod.CtrlCmd | KeyCode.KeyO`).
    """

    primary: Optional[KeyEncoding] = Field(
        None, description="(Optional) Key combo, (e.g. Ctrl+O)."
    )
    win: Optional[KeyEncoding] = Field(
        None, description="(Optional) Windows specific key combo."
    )
    mac: Optional[KeyEncoding] = Field(
        None, description="(Optional) MacOS specific key combo."
    )
    linux: Optional[KeyEncoding] = Field(
        None, description="(Optional) Linux specific key combo."
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

    # These methods are here to make KeyBindingRule work as a field
    # there are better ways to do this now with pydantic v2... but it still
    # feels a bit in flux.  pydantic_compat might not yet work for this (or
    # at least in my playing around i couldn't get it)
    # so sticking with this one conditional method here...
    if PYDANTIC2:
        # for v2
        @model_validator(mode="wrap")
        @classmethod
        def _model_val(
            cls: Type[M], v: Any, handler: Callable[[Any], M]
        ) -> "KeyBindingRule":
            if isinstance(v, StandardKeyBinding):
                return v.to_keybinding_rule()
            return handler(v)  # type: ignore

    else:

        @classmethod
        def validate(cls, value: Any) -> "KeyBindingRule":
            """Validate keybinding rule."""
            if isinstance(value, StandardKeyBinding):
                return value.to_keybinding_rule()
            return super().validate(value)


class KeyBindingRuleDict(TypedDict, total=False):
    """Typed dict for KeyBindingRule kwargs."""

    primary: Optional[str]
    win: Optional[str]
    linux: Optional[str]
    mac: Optional[str]
    weight: int
    when: Optional[expressions.Expr]


KeyBindingRuleOrDict = Union[KeyBindingRule, KeyBindingRuleDict]
