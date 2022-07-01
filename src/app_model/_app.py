from __future__ import annotations

from typing import TYPE_CHECKING, Callable, ClassVar, Dict, List, Tuple

from .registries import (
    CommandsRegistry,
    KeybindingsRegistry,
    MenusRegistry,
    register_action,
)

if TYPE_CHECKING:
    from .types import CommandIdStr


class Application:
    """Full application model."""

    _instances: ClassVar[Dict[str, Application]] = {}

    def __init__(self, name: str) -> None:
        self._name = name
        self.keybindings = KeybindingsRegistry()
        self.menus = MenusRegistry()
        self.commands = CommandsRegistry()
        self._disposers: List[Tuple[CommandIdStr, Callable[[], None]]] = []

    @classmethod
    def get_or_create(cls, name: str) -> Application:
        """Get app named `name` or create and return a new one if it doesn't exist."""
        if name not in cls._instances:
            cls._instances[name] = cls(name)
        return cls._instances[name]

    @property
    def name(self) -> str:
        """Return the name of the app."""
        return self._name

    def register_action(self, *args, **kwargs) -> Callable[[], None]:
        """Register an action and return a dispose function."""
        return register_action(self, *args, **kwargs)

    def dispose(self) -> None:
        """Dispose of the app."""
        for _, dispose in self._disposers:
            dispose()
        self._disposers.clear()
