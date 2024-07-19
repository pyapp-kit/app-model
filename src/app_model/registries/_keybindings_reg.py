from __future__ import annotations

from typing import TYPE_CHECKING, Callable, NamedTuple

from psygnal import Signal

from app_model.types import KeyBinding

if TYPE_CHECKING:
    from typing import Iterator, TypeVar

    from app_model import expressions
    from app_model.types import Action, DisposeCallable, KeyBindingRule

    CommandDecorator = Callable[[Callable], Callable]
    CommandCallable = TypeVar("CommandCallable", bound=Callable)


class _RegisteredKeyBinding(NamedTuple):
    """Internal object representing a fully registered keybinding."""

    keybinding: KeyBinding  # the keycode to bind to
    command_id: str  # the command to run
    weight: int  # the weight of the binding, for prioritization
    when: expressions.Expr | None = None  # condition to enable keybinding


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

    def __init__(self) -> None:
        self._keybindings: list[_RegisteredKeyBinding] = []
        self._filter_keybinding: Callable[[KeyBinding], str] | None = None

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
