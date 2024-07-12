"""App-model types."""

from typing import TYPE_CHECKING

from ._action import Action
from ._command_rule import CommandRule, ToggleRule
from ._constants import OperatingSystem
from ._icon import Icon
from ._keybinding_rule import KeyBindingRule
from ._keys import (
    KeyBinding,
    KeyChord,
    KeyCode,
    KeyCombo,
    KeyMod,
    SimpleKeyBinding,
    StandardKeyBinding,
)
from ._menu_rule import MenuItem, MenuItemBase, MenuRule, SubmenuItem

if TYPE_CHECKING:
    from typing import Callable, TypeAlias

    from ._icon import IconOrDict as IconOrDict
    from ._keybinding_rule import KeyBindingRuleDict as KeyBindingRuleDict
    from ._keybinding_rule import KeyBindingRuleOrDict as KeyBindingRuleOrDict
    from ._menu_rule import MenuOrSubmenu as MenuOrSubmenu
    from ._menu_rule import MenuRuleDict as MenuRuleDict
    from ._menu_rule import MenuRuleOrDict as MenuRuleOrDict

    # function that can be called without arguments to dispose of a resource
    DisposeCallable: TypeAlias = Callable[[], None]


__all__ = [
    "Action",
    "CommandRule",
    "Icon",
    "KeyBinding",
    "KeyBindingRule",
    "KeyChord",
    "KeyCode",
    "KeyCombo",
    "KeyMod",
    "OperatingSystem",
    "MenuItem",
    "MenuItemBase",
    "MenuRule",
    "ScanCode",
    "SimpleKeyBinding",
    "StandardKeyBinding",
    "SubmenuItem",
    "ToggleRule",
]
