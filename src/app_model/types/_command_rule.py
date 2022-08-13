from typing import Any, Callable, Optional, Union

from pydantic import Field

from .. import expressions
from ._base import _StrictModel
from ._icon import Icon


class ToggleRule(_StrictModel):
    """More detailed description of a toggle rule."""

    condition: Optional[expressions.Expr] = Field(
        None,
        description="(Optional) Condition under which the command should appear "
        "checked/toggled in any GUI representation (like a menu or button).",
    )
    initialize: Optional[Callable[[], bool]] = Field(
        None,
        description="Function to be called when a menu item/button is first created "
        "for this command. Must take no arguments and return a bool.",
    )
    experimental_connect: Optional[Callable[[Any], Any]] = Field(
        None,
        description="Experimental! Function to be called when a menu item/button is "
        "first created. Must take a single argument (the backend object, e.g. a "
        "`QAction`) and may perform signal connection. Since this exposes the backend, "
        "this field may be removed in the future.",
    )


class CommandRule(_StrictModel):
    """Data representing a command and its presentation.

    Presentation of contributed commands depends on the containing menu. The Command
    Palette, for instance, prefixes commands with their category, allowing for easy
    grouping. However, the Command Palette doesn't show icons nor disabled commands.
    Menus, on the other hand, shows disabled items as grayed out, but don't show the
    category label.
    """

    id: str = Field(..., description="A global identifier for the command.")
    title: str = Field(
        ...,
        description="Title by which the command is represented in the UI.",
    )
    category: Optional[str] = Field(
        None,
        description="(Optional) Category string by which the command may be grouped "
        "in the UI",
    )
    tooltip: Optional[str] = Field(
        None, description="(Optional) Tooltip to show when hovered."
    )
    status_tip: Optional[str] = Field(
        None,
        description="(Optional) Help message to show in the status bar when a "
        "button representing this command is hovered (For backends that support it).",
    )
    icon: Optional[Icon] = Field(
        None,
        description="(Optional) Icon used to represent this command, e.g. on buttons "
        "or in menus. These may be superqt fonticon keys, such as `fa6s.arrow_down`",
    )
    enablement: Optional[expressions.Expr] = Field(
        None,
        description="(Optional) Condition which must be true to enable the command in "
        "the UI (menu and keybindings). Does not prevent executing the command by "
        "other means, like the `execute_command` API.",
    )
    short_title: Optional[str] = Field(
        None,
        description="(Optional) Short title by which the command is represented in "
        "the UI. Menus pick either `title` or `short_title` depending on the context "
        "in which they show commands.",
    )
    toggled: Union[expressions.Expr, ToggleRule, None] = Field(
        None,
        description="(Optional) Condition under which the command should appear "
        "checked/toggled in any GUI representation (like a menu or button).",
    )

    def _as_command_rule(self) -> "CommandRule":
        """Simplify (subclasses) to a plain CommandRule."""
        return CommandRule(**{f: getattr(self, f) for f in CommandRule.__fields__})
