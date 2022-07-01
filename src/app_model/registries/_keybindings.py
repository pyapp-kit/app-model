from __future__ import annotations

from typing import TYPE_CHECKING, Callable, NamedTuple, Optional

from psygnal import Signal

if TYPE_CHECKING:
    from typing import Iterator, List, TypeVar

    from .. import expressions
    from ..types import CommandIdStr, KeybindingRule, KeyCodeStr

    DisposeCallable = Callable[[], None]
    CommandDecorator = Callable[[Callable], Callable]
    CommandCallable = TypeVar("CommandCallable", bound=Callable)


class _RegisteredKeyBinding(NamedTuple):
    """Internal object representing a fully registered keybinding."""

    keybinding: KeyCodeStr  # the keycode to bind to
    command_id: CommandIdStr  # the command to run
    weight: int  # the weight of the binding, for prioritization
    when: Optional[expressions.Expr] = None  # condition to enable keybinding


class KeybindingsRegistry:
    """Registery for keybindings."""

    registered = Signal()

    def __init__(self) -> None:
        self._keybindings: List[_RegisteredKeyBinding] = []

    def register_keybinding_rule(
        self, id: CommandIdStr, rule: KeybindingRule
    ) -> Optional[DisposeCallable]:
        """Register a new keybinding rule.

        Parameters
        ----------
        id : CommandIdStr
            Command identifier that should be run when the keybinding is triggered
        rule : KeybindingRule
            Keybinding information

        Returns
        -------
        Optional[DisposeCallable]
            A callable that can be used to unregister the keybinding
        """
        if bound_keybinding := rule._bind_to_current_platform():
            entry = _RegisteredKeyBinding(
                keybinding=bound_keybinding,
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
