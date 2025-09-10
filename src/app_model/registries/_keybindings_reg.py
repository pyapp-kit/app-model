from __future__ import annotations

from bisect import insort_left
from collections import defaultdict
from typing import TYPE_CHECKING, Callable, NamedTuple

from psygnal import Signal

from app_model.types import KeyBinding

if TYPE_CHECKING:
    from collections.abc import Iterable, Iterator, Mapping
    from typing import TypeVar

    from app_model import expressions
    from app_model.types import (
        Action,
        DisposeCallable,
        KeyBindingRule,
        KeyBindingSource,
    )

    CommandDecorator = Callable[[Callable], Callable]
    CommandCallable = TypeVar("CommandCallable", bound=Callable)


class _RegisteredKeyBinding(NamedTuple):
    """Internal object representing a fully registered keybinding."""

    keybinding: KeyBinding  # the keycode to bind to
    command_id: str  # the command to run
    weight: int  # the weight of the binding, for prioritization
    source: KeyBindingSource  # who defined the binding, for prioritization
    when: expressions.Expr | None = None  # condition to enable keybinding

    def __gt__(self, other: object) -> bool:
        if not isinstance(other, _RegisteredKeyBinding):
            return NotImplemented
        return (self.source, self.weight) > (other.source, other.weight)

    def __lt__(self, other: object) -> bool:
        if not isinstance(other, _RegisteredKeyBinding):
            return NotImplemented
        return (self.source, self.weight) < (other.source, other.weight)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, _RegisteredKeyBinding):
            return NotImplemented
        return (self.source, self.weight) == (other.source, other.weight)


class KeyBindingsRegistry:
    """Registry for keybindings.

    Attributes
    ----------
    filter_keybinding : Callable[[KeyBinding], str] | None
        Optional function for applying additional `KeyBinding` filtering.
        Callable should accept a `KeyBinding` object and return an error message
        (`str`) if `KeyBinding` is rejected, or empty string otherwise.
    """

    registered = Signal()
    unregistered = Signal()

    def __init__(self) -> None:
        self._keymap = defaultdict[int, list[_RegisteredKeyBinding]](list)
        self._filter_keybinding: Callable[[KeyBinding], str] | None = None

    @property
    def _keybindings(self) -> Iterable[_RegisteredKeyBinding]:
        return (entry for entries in self._keymap.values() for entry in entries)

    @property
    def filter_keybinding(self) -> Callable[[KeyBinding], str] | None:
        """Return the `filter_keybinding`."""
        return self._filter_keybinding

    @filter_keybinding.setter
    def filter_keybinding(self, value: Callable[[KeyBinding], str] | None) -> None:
        if callable(value) or value is None:
            self._filter_keybinding = value
        else:
            raise TypeError("'filter_keybinding' must be a callable or None")

    def register_action_keybindings(self, action: Action) -> DisposeCallable | None:
        """Register all keybindings declared in `action.keybindings`.

        Parameters
        ----------
        action : Action
            The action to register keybindings for.

        Returns
        -------
        DisposeCallable | None
            A function that can be called to unregister the keybindings.  If no
            keybindings were registered, returns None.
        """
        if not (keybindings := action.keybindings):
            return None

        disposers: list[Callable[[], None]] = []
        msg: list[str] = []
        for keyb in keybindings:
            if action.enablement is not None:
                kwargs = keyb.model_dump()
                kwargs["when"] = (
                    action.enablement
                    if keyb.when is None
                    else action.enablement | keyb.when
                )
                _keyb = type(keyb)(**kwargs)
            else:
                _keyb = keyb

            try:
                if d := self.register_keybinding_rule(action.id, _keyb):
                    disposers.append(d)
            except ValueError as e:
                msg.append(str(e))
        if msg:
            raise ValueError(
                "The following keybindings were not valid:\n" + "\n".join(msg)
            )

        if not disposers:  # pragma: no cover
            return None

        def _dispose() -> None:
            for disposer in disposers:
                disposer()

        return _dispose

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
            # list registry
            keybinding = KeyBinding.validate(plat_keybinding)
            if self._filter_keybinding:
                msg = self._filter_keybinding(keybinding)
                if msg:
                    raise ValueError(f"{keybinding}: {msg}")
            entry = _RegisteredKeyBinding(
                keybinding=keybinding,
                command_id=id,
                weight=rule.weight,
                when=rule.when,
                source=rule.source,
            )

            # inverse map registry
            entries = self._keymap[keybinding.to_int()]
            insort_left(entries, entry)

            self.registered.emit()

            def _dispose() -> None:
                # inverse map registry remove
                entries.remove(entry)
                self.unregistered.emit()
                if len(entries) == 0:
                    del self._keymap[keybinding.to_int()]

            return _dispose
        return None  # pragma: no cover

    def __iter__(self) -> Iterator[_RegisteredKeyBinding]:
        yield from self._keybindings

    def __len__(self) -> int:
        return sum(len(entries) for entries in self._keymap.values())

    def __repr__(self) -> str:
        name = self.__class__.__name__
        return f"<{name} at {hex(id(self))} ({len(self)} bindings)>"

    def get_keybinding(self, command_id: str) -> _RegisteredKeyBinding | None:
        """Return the first keybinding that matches the given command ID."""
        # TODO: improve me.
        matches = (kb for kb in self._keybindings if kb.command_id == command_id)
        sorted_matches = sorted(matches, key=lambda x: x.source, reverse=True)
        return next(iter(sorted_matches), None)

    def get_context_prioritized_keybinding(
        self, key: int, context: Mapping[str, object]
    ) -> _RegisteredKeyBinding | None:
        """
        Return the first keybinding that matches the given key sequence.

        The keybinding should be enabled given the context to be returned.

        Parameters
        ----------
        key : int
            The key sequence that represent the keybinding.
        context : Mapping[str, object]
            Variable context to parse the `when` expression to determine if the
            keybinding is enabled or not.

        Returns
        -------
        _RegisteredKeyBinding | None
            The keybinding found or None otherwise.

        """
        if key in self._keymap:
            for entry in reversed(self._keymap[key]):
                if entry.when is None or entry.when.eval(context):
                    return entry
        return None
