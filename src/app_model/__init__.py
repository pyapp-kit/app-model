"""Generic application schema implemented in python."""

from importlib.metadata import PackageNotFoundError, version

try:
    __version__ = version("app-model")
except PackageNotFoundError:
    __version__ = "uninstalled"
__author__ = "Talley Lambert"
__email__ = "talley.lambert@gmail.com"


from ._register_action import register_action
from ._registries import CommandsRegistry, KeybindingsRegistry, MenusRegistry
from ._types import Action

__all__ = [
    "Action",
    "CommandsRegistry",
    "KeybindingsRegistry",
    "NapariMenuGroup",
    "NapariMenu",
    "MenusRegistry",
    "register_action",
]
