"""App-model registries, such as menus, keybindings, commands."""
from ._commands import CommandsRegistry
from ._keybindings import KeybindingsRegistry
from ._menus import MenusRegistry
from ._register import register_action

__all__ = [
    "CommandsRegistry",
    "KeybindingsRegistry",
    "MenusRegistry",
    "register_action",
]
