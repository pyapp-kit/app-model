from collections.abc import Callable
from typing import Any, TypeAlias, TypedDict, TypeVar

from pydantic import Field, model_validator

from app_model import expressions

from ._base import _BaseModel
from ._constants import KeyBindingSource, OperatingSystem
from ._keys import StandardKeyBinding

KeyEncoding: TypeAlias = int | str
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

    primary: KeyEncoding | None = Field(
        default=None, description="(Optional) Key combo, (e.g. Ctrl+O)."
    )
    win: KeyEncoding | None = Field(
        default=None, description="(Optional) Windows specific key combo."
    )
    mac: KeyEncoding | None = Field(
        default=None, description="(Optional) MacOS specific key combo."
    )
    linux: KeyEncoding | None = Field(
        default=None, description="(Optional) Linux specific key combo."
    )
    when: expressions.Expr | None = Field(
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

    def _bind_to_current_platform(self) -> KeyEncoding | None:
        if _WIN and self.win:
            return self.win
        if _MAC and self.mac:
            return self.mac
        if _LINUX and self.linux:
            return self.linux
        return self.primary

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

    primary: str | None
    win: str | None
    linux: str | None
    mac: str | None
    weight: int
    when: expressions.Expr | None


KeyBindingRuleOrDict: TypeAlias = KeyBindingRule | KeyBindingRuleDict
