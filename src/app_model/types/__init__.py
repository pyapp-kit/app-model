"""App-model types."""
from ._action import Action
from ._command_rule import CommandRule
from ._icon import Icon, IconOrDict
from ._keybinding_rule import KeyBindingRule, KeyBindingRuleDict, KeyBindingRuleOrDict
from ._keys import KeyBinding, KeyChord, KeyCode, KeyMod, SimpleKeyBinding
from ._menu_rule import (
    MenuItem,
    MenuOrSubmenu,
    MenuRule,
    MenuRuleDict,
    MenuRuleOrDict,
    SubmenuItem,
)

__all__ = [
    "Action",
    "CommandRule",
    "Icon",
    "IconOrDict",
    "KeyBinding",
    "KeyBindingRule",
    "KeyBindingRuleDict",
    "KeyBindingRuleOrDict",
    "KeyChord",
    "KeyCode",
    "KeyMod",
    "MenuItem",
    "MenuOrSubmenu",
    "MenuRule",
    "MenuRuleDict",
    "MenuRuleOrDict",
    "ScanCode",
    "SimpleKeyBinding",
    "SubmenuItem",
]
