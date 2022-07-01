"""App-model types."""
from ._action import Action
from ._command import CommandIdStr, CommandRule
from ._icon import Icon, IconCodeStr, IconOrDict
from ._keybinding import (
    KeybindingRule,
    KeybindingRuleDict,
    KeybindingRuleOrDict,
    KeyCodeStr,
)
from ._menu import (
    MenuIdStr,
    MenuItem,
    MenuOrSubmenu,
    MenuRule,
    MenuRuleDict,
    MenuRuleOrDict,
    SubmenuItem,
)

__all__ = [
    "Action",
    "CommandIdStr",
    "CommandRule",
    "Icon",
    "IconCodeStr",
    "IconOrDict",
    "KeybindingRule",
    "KeybindingRuleDict",
    "KeybindingRuleOrDict",
    "KeyCodeStr",
    "MenuIdStr",
    "MenuItem",
    "MenuOrSubmenu",
    "MenuRule",
    "MenuRuleDict",
    "MenuRuleOrDict",
    "SubmenuItem",
]
