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
    """Full application model.

    This is the top level object that comprises all of the registries, and other
    app-namespace specific objects.

    ## Attributes:
    - `commands`: A [`CommandsRegistry`][app_model.registries.CommandsRegistry]
    - `menus`: A [`MenusRegistry`][app_model.registries.MenusRegistry]
    - `keybindings`: A [`KeyBindingsRegistry`][app_model.registries.KeyBindingsRegistry]
    - `injection_store`: An instance of an
      [in_n_out](https://github.com/tlambert03/in-n-out) `Store`
    """

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
        self._injection_store = ino.Store.create(name)

        self._commands = CommandsRegistry(self.injection_store)
        self._menus = MenusRegistry()
        self._keybindings = KeyBindingsRegistry()

        self.injection_store.on_unannotated_required_args = "ignore"

        self._disposers: List[Tuple[str, DisposeCallable]] = []

    @property
    def commands(self) -> CommandsRegistry:
        """Return the [`CommandsRegistry`][app_model.registries.CommandsRegistry]."""
        return self._commands

    @property
    def menus(self) -> MenusRegistry:
        """Return the [`MenusRegistry`][app_model.registries.MenusRegistry]."""
        return self._menus

    @property
    def keybindings(self) -> KeyBindingsRegistry:
        """Return the [`KeyBindingsRegistry`][app_model.registries.KeyBindingsRegistry]."""  # noqa
        return self._keybindings

    @property
    def injection_store(self) -> ino.Store:
        """Return the `in_n_out.Store` instance associated with this `Application`."""
        return self._injection_store

    @classmethod
    def get_or_create(cls, name: str) -> Application:
        """Get app named `name` or create and return a new one if it doesn't exist."""
        return cls._instances[name] if name in cls._instances else cls(name)

    @classmethod
    def destroy(cls, name: str) -> None:
        """Destroy the `Application` named `name`.

        This will call [`dispose()`][app_model.Application.dispose], destroy the
        injection store, and remove the application from the list of stored
        application names (allowing the name to be reused).
        """
        if name not in cls._instances:
            return
        app = cls._instances.pop(name)
        app.dispose()
        app.injection_store.destroy(name)
        app.destroyed.emit(app.name)

    @property
    def name(self) -> str:
        """Return the name of this `Application`."""
        return self._name

    def __repr__(self) -> str:
        return f"Application({self.name!r})"

    def dispose(self) -> None:
        """Dispose this `Application`.

        This calls all disposers functions (clearing all registries).
        """
        for _, dispose in self._disposers:
            dispose()
        self._disposers.clear()

    def register_action(self, action: Action) -> DisposeCallable:
        """Register [`Action`][app_model.Action] instance with this application.

        An [`Action`][app_model.Action] is the complete representation of a command,
        including information about where and whether it appears in menus and optional
        keybinding rules.

        This returns a function that may be called to undo the registration of `action`.
        """
        return register_action(self, id_or_action=action)
