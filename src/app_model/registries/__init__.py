"""App-model registries, such as menus, keybindings, commands."""

from ._commands_reg import CommandsRegistry, RegisteredCommand
from ._keybindings_reg import KeyBindingsRegistry
from ._menus_reg import MenusRegistry
from ._register import register_action

__all__ = [
    "CommandsRegistry",
    "KeyBindingsRegistry",
    "MenusRegistry",
    "register_action",
    "RegisteredCommand",
]
