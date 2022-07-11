from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar, Dict, List, Tuple

import in_n_out as ino
from psygnal import Signal

from .registries import (
    CommandsRegistry,
    KeyBindingsRegistry,
    MenusRegistry,
    register_action,
)

if TYPE_CHECKING:
    from .types import Action
    from .types._constants import DisposeCallable


class Application:
    """Full application model."""

    destroyed = Signal(str)
    _instances: ClassVar[Dict[str, Application]] = {}

    def __init__(self, name: str) -> None:
        self._name = name
        if name in Application._instances:
            raise ValueError(
                f"Application {name!r} already exists. Retrieve it with "
                f"`Application.get_or_create({name!r})`."
            )
        Application._instances[name] = self
        self.injection_store = ino.Store.create(name)

        self.keybindings = KeyBindingsRegistry()
        self.menus = MenusRegistry()
        self.commands = CommandsRegistry(self.injection_store)

        self.injection_store.on_unannotated_required_args = "ignore"

        self._disposers: List[Tuple[str, DisposeCallable]] = []

    @classmethod
    def get_or_create(cls, name: str) -> Application:
        """Get app named `name` or create and return a new one if it doesn't exist."""
        return cls._instances[name] if name in cls._instances else cls(name)

    @classmethod
    def destroy(cls, name: str) -> None:
        """Destroy the app named `name`."""
        app = cls._instances.pop(name)
        app.dispose()
        app.injection_store.destroy(name)
        app.destroyed.emit(app.name)

    @property
    def name(self) -> str:
        """Return the name of the app."""
        return self._name

    def __repr__(self) -> str:
        return f"Application({self.name!r})"

    def dispose(self) -> None:
        """Dispose of the app."""
        for _, dispose in self._disposers:
            dispose()
        self._disposers.clear()

    def register_action(self, action: Action) -> DisposeCallable:
        """Register `action` with this application.

        See docs for register_action() in app_model.registries
        """
        return register_action(self, id_or_action=action)
