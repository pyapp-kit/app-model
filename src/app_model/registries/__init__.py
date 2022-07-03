"""App-model registries, such as menus, keybindings, commands."""
from ._commands import CommandsRegistry
from ._keybindings import KeyBindingsRegistry
from ._menus import MenusRegistry
from ._register import register_action

__all__ = [
    "CommandsRegistry",
    "KeyBindingsRegistry",
    "MenusRegistry",
    "register_action",
]
