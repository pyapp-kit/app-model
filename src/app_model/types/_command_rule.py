from typing import Callable, Optional, Union

from pydantic_compat import Field

from app_model import expressions

from ._base import _BaseModel
from ._icon import Icon


class ToggleRule(_BaseModel):
    """More detailed description of a toggle rule."""

    condition: Optional[expressions.Expr] = Field(
        None,
        description="(Optional) Condition under which the command should appear "
        "checked/toggled in any GUI representation (like a menu or button).",
    )
    get_current: Optional[Callable[[], bool]] = Field(
        None,
        description="Function that returns the current state of the toggle.",
    )


class CommandRule(_BaseModel):
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
        "button representing this command is hovered (for backends that support it).",
    )
    icon: Optional[Icon] = Field(
        None,
        description="(Optional) Icon used to represent this command, e.g. on buttons "
        "or in menus. These may be [iconify keys](https://icon-sets.iconify.design), "
        "such as `fa6-solid:arrow-down`, or "
        "[superqt.fonticon](https://pyapp-kit.github.io/superqt/utilities/fonticon/)"
        " keys, such as `fa6s.arrow_down`, or a path to a local `.svg` file using the "
        "[file URI scheme](https://en.wikipedia.org/wiki/File_URI_scheme). "
        "Note that on Windows the file URI scheme should always start with "
        "`file:///` (three slashes)",
    )
    icon_visible_in_menu: bool = Field(
        True,
        description="Whether to show the icon in menus (for backends that support it). "
        "If `False`, only the title will be shown. By default, `True`.",
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
    toggled: Union[ToggleRule, expressions.Expr, None] = Field(
        None,
        description="(Optional) Condition under which the command should appear "
        "checked/toggled in any GUI representation (like a menu or button).",
    )

    def _as_command_rule(self) -> "CommandRule":
        """Simplify (subclasses) to a plain CommandRule."""
        return CommandRule(**{f: getattr(self, f) for f in CommandRule.__annotations__})
