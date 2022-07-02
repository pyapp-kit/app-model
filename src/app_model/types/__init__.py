"""App-model types."""
from ._action import Action
from ._command import CommandIdStr, CommandRule
from ._icon import Icon, IconCodeStr, IconOrDict
from ._key_codes import KeyCode, ScanCode
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
    "KeyCode",
    "KeyCodeStr",
    "MenuIdStr",
    "MenuItem",
    "MenuOrSubmenu",
    "MenuRule",
    "MenuRuleDict",
    "MenuRuleOrDict",
    "ScanCode",
    "SubmenuItem",
]
