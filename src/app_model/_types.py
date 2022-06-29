from __future__ import annotations

import os
import sys
from functools import cached_property
from typing import (
    TYPE_CHECKING,
    Any,
    Callable,
    Generator,
    Generic,
    List,
    NamedTuple,
    NewType,
    Optional,
    TypedDict,
    TypeVar,
)

from pydantic import BaseModel, Field

from . import context

WINDOWS = os.name == "nt"
MACOS = sys.platform == "darwin"
LINUX = sys.platform.startswith("linux")

CommandIdStr = NewType("CommandIdStr", str)
MenuIdStr = NewType("MenuIdStr", str)
KeyCodeStr = NewType("KeyCodeStr", str)
IconCodeStr = NewType("IconCodeStr", str)
CommandCallable = TypeVar("CommandCallable", bound=Callable[..., Any])

if TYPE_CHECKING:

    # Typed dicts mimic the API of their pydantic counterparts.
    # Since pydantic allows you to pass in either an object or a dict,
    # This lets us use either anywhere, without losing typing support.
    # e.g. Union[MenuRuleDict, MenuRule]
    class MenuRuleDict(TypedDict, total=False):
        """Typed dict for MenuRule kwargs."""

        when: Optional[context.Expr]
        group: str
        order: Optional[float]
        id: MenuIdStr

    class KeybindingRuleDict(TypedDict, total=False):
        """Typed dict for KeybindingRule kwargs."""

        primary: Optional[KeyCodeStr]
        win: Optional[KeyCodeStr]
        linux: Optional[KeyCodeStr]
        mac: Optional[KeyCodeStr]
        weight: int
        when: Optional[context.Expr]


# ------------------ commands-related types --------------------


class Icon(BaseModel):
    """Icons used to represent commands, or submenus.

    May provide both a light and dark variant.  If only one is provided, it is used
    in all theme types.
    """

    dark: Optional[IconCodeStr] = Field(
        None,
        description="Icon path when a dark theme is used. These may be superqt "
        "fonticon keys, such as `fa5s.arrow_down`",
    )
    light: Optional[IconCodeStr] = Field(
        None,
        description="Icon path when a light theme is used. These may be superqt "
        "fonticon keys, such as `fa5s.arrow_down`",
    )

    @classmethod
    def __get_validators__(cls) -> Generator[Callable[..., Any], None, None]:
        yield cls.validate

    @classmethod
    def validate(cls, v: Any) -> Icon:
        """Validate icon."""
        if isinstance(v, str):
            v = {"dark": v, "light": v}
        return cls(**v)


class CommandRule(BaseModel):
    """Data representing a command and its presentation.

    Presentation of contributed commands depends on the containing menu. The Command
    Palette, for instance, prefixes commands with their category, allowing for easy
    grouping. However, the Command Palette doesn't show icons nor disabled commands.
    Menus, on the other hand, shows disabled items as grayed out, but don't show the
    category label.
    """

    id: CommandIdStr = Field(..., description="The global identifier for the command.")
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
    icon: Optional[Icon] = Field(
        None,
        description="(Optional) Icon used to represent this command, e.g. on buttons "
        "or in menus. These may be superqt fonticon keys, such as `fa5s.arrow_down`",
    )
    enablement: Optional[context.Expr] = Field(
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


class _RegisteredCommand:
    """Small object to represent a command in the CommandsRegistry.

    Only used internally by the CommandsRegistry.
    This helper class allows us to cache the dependency-injected variant of the
    command. As usual with `cached_property`, the cache can be cleard by deleting
    the attribute: `del cmd.run_injected`
    """

    def __init__(self, id: CommandIdStr, run: CommandCallable, title: str) -> None:
        self.id = id
        self.run = run
        self.title = title

    @cached_property
    def run_injected(self) -> Callable:
        # from .._injection import inject_dependencies
        # return inject_dependencies(self.run)
        return self.run


# ------------------ keybinding-related types --------------------


class KeybindingRule(BaseModel):
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
    when: Optional[context.Expr] = Field(
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


class _RegisteredKeyBinding(NamedTuple):
    """Internal object representing a fully registered keybinding."""

    keybinding: KeyCodeStr  # the keycode to bind to
    command_id: CommandIdStr  # the command to run
    weight: int  # the weight of the binding, for prioritization
    when: Optional[context.Expr] = None  # condition to enable keybinding


# ------------------ menus-related types --------------------


class _MenuItemBase(BaseModel):
    """Data representing where and when a menu item should be shown."""

    when: Optional[context.Expr] = Field(
        None,
        description="(Optional) Condition which must be true to show the item.",
    )
    group: Optional[str] = Field(
        None,
        description="(Optional) Menu group to which this item should be added. Menu "
        "groups are sortable strings (like `'1_cutandpaste'`). 'navigation' is a "
        "special group that always appears at the top of a menu.  If not provided, "
        "the item is added in the last group of the menu.",
    )
    order: Optional[float] = Field(
        None,
        description="(Optional) Order of the item *within* its group. Note, order is "
        "not part of the plugin schema, plugins may provide it using the group key "
        "and the syntax 'group@order'.  If not provided, items are sorted by title.",
    )


class MenuRule(_MenuItemBase):
    """A MenuRule defines a menu location and conditions for presentation.

    It does not define an actual command. That is done in either `MenuItem` or `Action`.
    """

    id: MenuIdStr = Field(..., description="Menu in which to place this item.")


class MenuItem(_MenuItemBase):
    """Combination of a Command and conditions for menu presentation.

    This object is mostly constructed by `register_action` right before menu item
    registration.
    """

    command: CommandRule = Field(
        ...,
        description="CommandRule to execute when this menu item is selected.",
    )
    alt: Optional[CommandRule] = Field(
        None,
        description="(Optional) Alternate command to execute when this menu item is "
        "selected, (e.g. when the Alt-key is held when opening the menu)",
    )


class SubmenuItem(_MenuItemBase):
    """Point to another Menu that will be displayed as a submenu."""

    submenu: MenuIdStr = Field(..., description="Menu to insert as a submenu.")
    title: str = Field(..., description="Title of this submenu, shown in the UI.")
    icon: Optional[Icon] = Field(
        None,
        description="(Optional) Icon used to represent this submenu. "
        "These may be superqt fonticon keys, such as `fa5s.arrow_down`",
    )


# ------------------ (complete) action-related types --------------------


class Action(CommandRule, Generic[CommandCallable]):
    """Callable object along with specific context, menu, keybindings logic.

    This is the "complete" representation of a command.  Including a pointer to the
    actual callable object, as well as any additional menu and keybinding rules.
    Most commands and menu items will be represented by Actions, and registered using
    `register_action`.
    """

    run: CommandCallable = Field(
        ...,
        description="A function to call when the associated command id is executed.",
    )
    menus: Optional[List[MenuRule]] = Field(
        None,
        description="(Optional) Menus to which this action should be added.",
    )
    keybindings: Optional[List[KeybindingRule]] = Field(
        None,
        description="(Optional) Default keybinding(s) that will trigger this command.",
    )
    add_to_command_palette: bool = Field(
        True,
        description="Whether to add this command to the global Command Palette "
        "during registration.",
    )
