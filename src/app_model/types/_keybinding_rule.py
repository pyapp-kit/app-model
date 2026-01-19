from typing import Any, Callable, Optional, TypedDict, TypeVar, Union

from pydantic import Field, model_validator

from app_model import expressions
from app_model.types._keys._keybindings import KeyBinding

from ._base import _BaseModel
from ._constants import KeyBindingSource, OperatingSystem
from ._keys import StandardKeyBinding

KeyEncoding = Union[int, str]
M = TypeVar("M")


class KeyBindingRule(_BaseModel):
    """Data representing a keybinding and when it should be active.

    This model lacks a corresponding command. That gets linked up elsewhere,
    such as below in `Action`.

    Values can be expressed as either a string (e.g. `"Ctrl+O"`) or an integer, using
    combinations of [`KeyMod`][app_model.types.KeyMod] and
    [`KeyCode`][app_model.types.KeyCode], (e.g. `KeyMod.CtrlCmd | KeyCode.KeyO`).
    """

    primary: Optional[KeyEncoding] = Field(
        default=None, description="(Optional) Key combo, (e.g. Ctrl+O)."
    )
    win: Optional[KeyEncoding] = Field(
        default=None, description="(Optional) Windows specific key combo."
    )
    mac: Optional[KeyEncoding] = Field(
        default=None, description="(Optional) MacOS specific key combo."
    )
    linux: Optional[KeyEncoding] = Field(
        default=None, description="(Optional) Linux specific key combo."
    )
    when: Optional[expressions.Expr] = Field(
        default=None,
        description="(Optional) Condition when the keybingding is active.",
    )
    weight: int = Field(
        default=0,
        description="Internal weight used to sort keybindings. "
        "This is not part of the plugin schema",
    )
    source: KeyBindingSource = Field(
        default=KeyBindingSource.APP,
        description="Who registered the keybinding. Used to sort keybindings.",
    )

    def to_keybinding(
        self, os: Optional[OperatingSystem] = None
    ) -> "Optional[KeyBinding]":
        """Return a keybinding for the given OS, or current OS if not specified."""
        if (enc := self.for_os(os)) is not None:
            if isinstance(enc, int):
                return KeyBinding.from_int(enc, os=os)
            elif isinstance(enc, str):
                return KeyBinding.from_str(enc)
            else:
                raise TypeError("invalid keybinding")  # pragma: no cover
        raise ValueError("No keybinding for platform")  # pragma: no cover

    def for_os(self, os: Optional[OperatingSystem] = None) -> Optional[KeyEncoding]:
        """Select the encoding for the given OS, or current OS if not specified."""
        if os is None:
            os = OperatingSystem.current()
        enc = {
            OperatingSystem.WINDOWS: self.win,
            OperatingSystem.MACOS: self.mac,
            OperatingSystem.LINUX: self.linux,
        }[os]
        if enc is None:
            return self.primary
        return enc

    @model_validator(mode="wrap")
    @classmethod
    def _model_val(
        cls: type[M], v: Any, handler: Callable[[Any], M]
    ) -> "KeyBindingRule":
        if isinstance(v, StandardKeyBinding):
            return v.to_keybinding_rule()
        return handler(v)  # type: ignore


class KeyBindingRuleDict(TypedDict, total=False):
    """Typed dict for KeyBindingRule kwargs."""

    primary: Optional[str]
    win: Optional[str]
    linux: Optional[str]
    mac: Optional[str]
    weight: int
    when: Optional[expressions.Expr]


KeyBindingRuleOrDict = Union[KeyBindingRule, KeyBindingRuleDict]
