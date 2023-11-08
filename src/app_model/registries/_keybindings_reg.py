from __future__ import annotations

from typing import TYPE_CHECKING, Callable, NamedTuple

from psygnal import Signal

from app_model.types import KeyBinding

if TYPE_CHECKING:
    from typing import Iterator, TypeVar

    from app_model import expressions
    from app_model.types import DisposeCallable, KeyBindingRule

    CommandDecorator = Callable[[Callable], Callable]
    CommandCallable = TypeVar("CommandCallable", bound=Callable)


class _RegisteredKeyBinding(NamedTuple):
    """Internal object representing a fully registered keybinding."""

    keybinding: KeyBinding  # the keycode to bind to
    command_id: str  # the command to run
    weight: int  # the weight of the binding, for prioritization
    when: expressions.Expr | None = None  # condition to enable keybinding


class KeyBindingsRegistry:
    """Registry for keybindings."""

    registered = Signal()

    def __init__(self) -> None:
        self._keybindings: list[_RegisteredKeyBinding] = []

    def register_keybinding_rule(
        self, id: str, rule: KeyBindingRule
    ) -> DisposeCallable | None:
        """Register a new keybinding rule.

        Parameters
        ----------
        id : str
            Command identifier that should be run when the keybinding is triggered
        rule : KeyBindingRule
            KeyBinding information

        Returns
        -------
        Optional[DisposeCallable]
            A callable that can be used to unregister the keybinding
        """
        if plat_keybinding := rule._bind_to_current_platform():
            keybinding = KeyBinding.validate(plat_keybinding)
            entry = _RegisteredKeyBinding(
                keybinding=keybinding,
                command_id=id,
                weight=rule.weight,
                when=rule.when,
            )
            self._keybindings.append(entry)
            self.registered.emit()

            def _dispose() -> None:
                self._keybindings.remove(entry)

            return _dispose
        return None  # pragma: no cover

    def __iter__(self) -> Iterator[_RegisteredKeyBinding]:
        yield from self._keybindings

    def __repr__(self) -> str:
        name = self.__class__.__name__
        return f"<{name} at {hex(id(self))} ({len(self._keybindings)} bindings)>"

    def get_keybinding(self, key: str) -> _RegisteredKeyBinding | None:
        """Return the first keybinding that matches the given command ID."""
        # TODO: improve me.
        return next(
            (entry for entry in self._keybindings if entry.command_id == key), None
        )
