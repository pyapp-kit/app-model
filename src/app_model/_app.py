from __future__ import annotations

import contextlib
from typing import (
    TYPE_CHECKING,
    ClassVar,
    Dict,
    List,
    Literal,
    Optional,
    Tuple,
    Union,
    overload,
)

from .registries import (
    CommandsRegistry,
    KeybindingsRegistry,
    MenusRegistry,
    register_action,
)

if TYPE_CHECKING:
    from . import expressions
    from .registries._commands import CommandCallable
    from .registries._register import CommandDecorator
    from .types import (
        Action,
        CommandIdStr,
        IconOrDict,
        KeybindingRuleOrDict,
        MenuRuleOrDict,
    )
    from .types._misc import DisposeCallable


class Application:
    """Full application model."""

    _instances: ClassVar[Dict[str, Application]] = {}

    def __init__(self, name: str) -> None:
        self._name = name
        if name in Application._instances:
            raise ValueError(
                f"Application {name!r} already exists. Retrieve it with "
                f"`Application.get_or_create({name!r})`."
            )
        Application._instances[name] = self

        self.keybindings = KeybindingsRegistry()
        self.menus = MenusRegistry()
        self.commands = CommandsRegistry()
        self._disposers: List[Tuple[CommandIdStr, DisposeCallable]] = []

    @classmethod
    def get_or_create(cls, name: str) -> Application:
        """Get app named `name` or create and return a new one if it doesn't exist."""
        return cls._instances[name] if name in cls._instances else cls(name)

    @classmethod
    def destroy(cls, name: str) -> None:
        """Destroy the app named `name`."""
        app = cls._instances.pop(name)
        app.dispose()

    def __del__(self) -> None:
        """Remove the app from the registry when it is garbage collected."""
        with contextlib.suppress(KeyError):
            Application.destroy(self.name)

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

    @overload
    def register_action(self, id_or_action: Action) -> DisposeCallable:
        ...

    @overload
    def register_action(
        self,
        id_or_action: CommandIdStr,
        title: str,
        *,
        callback: Literal[None] = None,
        category: Optional[str] = None,
        tooltip: Optional[str] = None,
        icon: Optional[IconOrDict] = None,
        enablement: Optional[expressions.Expr] = None,
        menus: Optional[List[MenuRuleOrDict]] = None,
        keybindings: Optional[List[KeybindingRuleOrDict]] = None,
        add_to_command_palette: bool = True,
    ) -> CommandDecorator:
        ...

    @overload
    def register_action(
        self,
        id_or_action: CommandIdStr,
        title: str,
        *,
        callback: CommandCallable,
        category: Optional[str] = None,
        tooltip: Optional[str] = None,
        icon: Optional[IconOrDict] = None,
        enablement: Optional[expressions.Expr] = None,
        menus: Optional[List[MenuRuleOrDict]] = None,
        keybindings: Optional[List[KeybindingRuleOrDict]] = None,
        add_to_command_palette: bool = True,
    ) -> DisposeCallable:
        ...

    def register_action(
        self,
        id_or_action: Union[CommandIdStr, Action],
        title: Optional[str] = None,
        *,
        callback: Optional[CommandCallable] = None,
        category: Optional[str] = None,
        tooltip: Optional[str] = None,
        icon: Optional[IconOrDict] = None,
        enablement: Optional[expressions.Expr] = None,
        menus: Optional[List[MenuRuleOrDict]] = None,
        keybindings: Optional[List[KeybindingRuleOrDict]] = None,
        add_to_command_palette: bool = True,
    ) -> Union[CommandDecorator, DisposeCallable]:
        """Register an action and return a dispose function."""
        return register_action(
            self,
            id_or_action,  # type: ignore
            title=title,  # type: ignore
            callback=callback,  # type: ignore
            category=category,
            tooltip=tooltip,
            icon=icon,
            enablement=enablement,
            menus=menus,
            keybindings=keybindings,
            add_to_command_palette=add_to_command_palette,
        )
