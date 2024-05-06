from __future__ import annotations

from concurrent.futures import Future, ThreadPoolExecutor
from typing import TYPE_CHECKING, Any, Callable, Generic, Iterator, TypeVar, cast

from in_n_out import Store
from psygnal import Signal

# maintain runtime compatibility with older typing_extensions
if TYPE_CHECKING:
    from typing_extensions import ParamSpec

    from app_model.types import Action, DisposeCallable

    P = ParamSpec("P")
else:
    try:
        from typing_extensions import ParamSpec

        P = ParamSpec("P")
    except ImportError:
        P = TypeVar("P")


R = TypeVar("R")


class RegisteredCommand(Generic[P, R]):
    """Small object to represent a command in the CommandsRegistry.

    Used internally by the CommandsRegistry.

    This helper class allows us to cache the dependency-injected variant of the
    command, so that type resolution and dependency injection is performed only
    once.
    """

    __slots__ = (
        "id",
        "callback",
        "title",
        "_resolved_callback",
        "_injection_store",
        "_injected_callback",
        "_initialized",
    )

    def __init__(
        self,
        id: str,
        callback: Callable[P, R] | str,
        title: str,
        store: Store | None = None,
    ) -> None:
        self.id = id
        self.callback = callback
        self.title = title
        self._injection_store: Store = store or Store.get_store()
        self._resolved_callback = callback if callable(callback) else None
        self._injected_callback: Callable[P, R] | None = None
        self._initialized = True

    def __setattr__(self, name: str, value: Any) -> None:
        """Object is immutable after initialization."""
        if getattr(self, "_initialized", False):
            raise AttributeError("RegisteredCommand object is immutable.")
        super().__setattr__(name, value)

    @property
    def resolved_callback(self) -> Callable[P, R]:
        """Return the resolved command callback.

        This property is cached, so the callback types are only resolved once.
        """
        if self._resolved_callback is None:
            from app_model.types._utils import import_python_name

            try:
                cb = import_python_name(str(self.callback))
            except ImportError as e:
                object.__setattr__(self, "_resolved_callback", lambda *a, **k: None)
                raise type(e)(
                    f"Command pointer {self.callback!r} registered for Command "
                    f"{self.id!r} was not importable: {e}"
                ) from e

            if not callable(cb):
                # don't try to import again, just create a no-op
                object.__setattr__(self, "_resolved_callback", lambda *a, **k: None)
                raise TypeError(
                    f"Command pointer {self.callback!r} registered for Command "
                    f"{self.id!r} did not resolve to a callble object."
                )
            object.__setattr__(self, "_resolved_callback", cb)
        return cast("Callable[P, R]", self._resolved_callback)

    @property
    def run_injected(self) -> Callable[P, R]:
        """Return the command callback with dependencies injected.

        This property is cached, so the injected version is only created once.
        """
        if self._injected_callback is None:
            cb = self._injection_store.inject(self.resolved_callback, processors=True)
            object.__setattr__(self, "_injected_callback", cb)
        return cast("Callable[P, R]", self._injected_callback)


class CommandsRegistry:
    """Registry for commands (callable objects)."""

    registered = Signal(str)

    def __init__(
        self,
        injection_store: Store | None = None,
        raise_synchronous_exceptions: bool = False,
    ) -> None:
        self._commands: dict[str, RegisteredCommand] = {}
        self._injection_store = injection_store
        self._raise_synchronous_exceptions = raise_synchronous_exceptions

    def register_action(self, action: Action) -> DisposeCallable:
        """Register an Action object.

        This is a convenience method that registers the action's callback
        with the action's ID and title using `register_command`.

        Parameters
        ----------
        action: Action
            Action to register

        Returns
        -------
        DisposeCallable
            A function that can be called to unregister the action.
        """
        return self.register_command(action.id, action.callback, action.title)

    def register_command(
        self, id: str, callback: Callable[P, R] | str, title: str
    ) -> DisposeCallable:
        """Register a callable as the handler for command `id`.

        Parameters
        ----------
        id : CommandId
            Command identifier
        callback : Callable
            Callable to be called when the command is executed
        title : str
            Title for the command.

        Returns
        -------
        DisposeCallable
            A function that can be called to unregister the command.
        """
        if id in self._commands:
            raise ValueError(
                f"Command {id!r} already registered with callback "
                f"{self._commands[id].callback!r} (new callback: {callback!r})"
            )

        cmd = RegisteredCommand(id, callback, title, self._injection_store)
        self._commands[id] = cmd

        def _dispose() -> None:
            self._commands.pop(id, None)

        self.registered.emit(id)
        return _dispose

    def __iter__(self) -> Iterator[tuple[str, RegisteredCommand]]:
        yield from self._commands.items()

    def __len__(self) -> int:
        return len(self._commands)

    def __contains__(self, id: str) -> bool:
        return id in self._commands

    def __repr__(self) -> str:
        name = self.__class__.__name__
        return f"<{name} at {hex(id(self))} ({len(self._commands)} commands)>"

    def __getitem__(self, id: str) -> RegisteredCommand:
        """Retrieve commands registered under a given ID."""
        if id not in self._commands:
            raise KeyError(f"Command {id!r} not registered")
        return self._commands[id]

    def execute_command(
        self,
        id: str,
        *args: Any,
        execute_asynchronously: bool = False,
        **kwargs: Any,
    ) -> Future:
        """Execute a registered command.

        Parameters
        ----------
        id : CommandId
            ID of the command to execute
        *args: Any
            Positional arguments to pass to the command
        execute_asynchronously : bool
            Whether to execute the command asynchronously in a thread,
            by default `False`.  Note that *regardless* of this setting,
            the return value will implement the `Future` API (so it's necessary)
            to call `result()` on the returned object.  Eventually, this will
            default to True, but we need to solve `ensure_main_thread` Qt threading
            issues first
        **kwargs: Any
            Keyword arguments to pass to the command

        Returns
        -------
        Future: concurrent.futures.Future
            Future object containing the result of the command

        Raises
        ------
        KeyError
            If the command is not registered or has no callbacks.
        """
        try:
            cmd = self[id].run_injected
        except KeyError as e:
            raise KeyError(f"Command {id!r} not registered") from e  # pragma: no cover

        if execute_asynchronously:
            with ThreadPoolExecutor() as executor:
                return executor.submit(cmd, *args, **kwargs)

        future: Future = Future()
        try:
            future.set_result(cmd(*args, **kwargs))
        except Exception as e:
            if self._raise_synchronous_exceptions:
                # note, the caller of this function can also achieve this by
                # calling `future.result()` on the returned future object.
                raise e
            future.set_exception(e)

        return future

    def __str__(self) -> str:
        lines = [f"{id_!r:<32} -> {cmd.title!r}" for id_, cmd in self]
        return "\n".join(lines)
