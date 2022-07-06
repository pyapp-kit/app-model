from typing import Any, Callable, Generator, Optional, Type, TypedDict, Union

from pydantic import Field

from .. import expressions
from ._base import _StrictModel
from ._command_rule import CommandRule
from ._icon import Icon


class _MenuItemBase(_StrictModel):
    """Data representing where and when a menu item should be shown."""

    when: Optional[expressions.Expr] = Field(
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

    @classmethod
    def __get_validators__(cls) -> Generator[Callable[..., Any], None, None]:
        yield cls.validate

    @classmethod
    def validate(cls: Type["_MenuItemBase"], v: Any) -> "_MenuItemBase":
        """Validate icon."""
        if isinstance(v, _MenuItemBase):
            return v
        if isinstance(v, dict):
            if "command" in v:
                return MenuItem(**v)
            if "id" in v:
                return MenuRule(**v)
            if "submenu" in v:
                return SubmenuItem(**v)
        raise TypeError(f"Invalid menu item: {v!r}", cls)  # pragma: no cover


class MenuRule(_MenuItemBase):
    """A MenuRule defines a menu location and conditions for presentation.

    It does not define an actual command. That is done in either `MenuItem` or `Action`.
    """

    id: str = Field(..., description="Menu in which to place this item.")


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

    submenu: str = Field(..., description="Menu to insert as a submenu.")
    title: str = Field(..., description="Title of this submenu, shown in the UI.")
    icon: Optional[Icon] = Field(
        None,
        description="(Optional) Icon used to represent this submenu. "
        "These may be superqt fonticon keys, such as `fa5s.arrow_down`",
    )
    enablement: Optional[expressions.Expr] = Field(
        None,
        description="(Optional) Condition which must be true to enable the submenu. "
        "Disabled submenus appear grayed out in the UI, and cannot be selected. By "
        "default, submenus are enabled.",
    )


class MenuRuleDict(TypedDict, total=False):
    """Typed dict for MenuRule kwargs.

    This mimics the pydantic `MenuRule` interface, but allows you to pass in a dict
    """

    when: Optional[expressions.Expr]
    group: str
    order: Optional[float]
    id: str


MenuRuleOrDict = Union[MenuRule, MenuRuleDict]
MenuOrSubmenu = Union[MenuItem, SubmenuItem]
