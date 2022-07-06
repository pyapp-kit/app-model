from __future__ import annotations

from concurrent.futures import Future, ThreadPoolExecutor
from functools import cached_property
from typing import TYPE_CHECKING, Any, Callable, Generic, Optional, TypeVar, Union, cast

from in_n_out import Store
from psygnal import Signal
from typing_extensions import ParamSpec

if TYPE_CHECKING:
    from typing import Dict, Iterator, List, Tuple

    DisposeCallable = Callable[[], None]

P = ParamSpec("P")
R = TypeVar("R")


class _RegisteredCommand(Generic[P, R]):
    """Small object to represent a command in the CommandsRegistry.

    Only used internally by the CommandsRegistry.
    This helper class allows us to cache the dependency-injected variant of the
    command. As usual with `cached_property`, the cache can be cleard by deleting
    the attribute: `del cmd.run_injected`
    """

    def __init__(
        self,
        id: str,
        callback: Union[str, Callable[P, R]],
        title: str,
        store: Optional[Store] = None,
    ) -> None:
        self.id = id
        self.callback = callback
        self.title = title
        self._resolved_callback = callback if callable(callback) else None
        self._injection_store: Store = store or Store.get_store()

    @property
    def resolved_callback(self) -> Callable[P, R]:
        if self._resolved_callback is None:
            from ..types._utils import import_python_name

            try:
                self._resolved_callback = import_python_name(str(self.callback))
            except ImportError as e:
                self._resolved_callback = cast(Callable[P, R], lambda *a, **k: None)
                raise type(e)(
                    f"Command pointer {self.callback!r} registered for Command "
                    f"{self.id!r} was not importable: {e}"
                ) from e

            if not callable(self._resolved_callback):
                # don't try to import again, just create a no-op
                self._resolved_callback = cast(Callable[P, R], lambda *a, **k: None)
                raise TypeError(
                    f"Command pointer {self.callback!r} registered for Command "
                    f"{self.id!r} did not resolve to a callble object."
                )
        return self._resolved_callback

    @cached_property
    def run_injected(self) -> Callable[P, R]:
        return self._injection_store.inject(self.resolved_callback, processors=True)


class CommandsRegistry:
    """Registry for commands (callable objects)."""

    registered = Signal(str)

    def __init__(self, injection_store: Optional[Store] = None) -> None:
        self._commands: Dict[str, List[_RegisteredCommand]] = {}
        self._injection_store = injection_store

    def register_command(
        self, id: str, callback: Union[str, Callable[P, R]], title: str
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
        commands = self._commands.setdefault(id, [])

        cmd = _RegisteredCommand(id, callback, title, self._injection_store)
        commands.insert(0, cmd)

        def _dispose() -> None:
            commands.remove(cmd)
            if not commands:
                del self._commands[id]

        self.registered.emit(id)
        return _dispose

    def __iter__(self) -> Iterator[Tuple[str, List[_RegisteredCommand]]]:
        yield from self._commands.items()

    def __contains__(self, id: str) -> bool:
        return id in self._commands

    def __repr__(self) -> str:
        name = self.__class__.__name__
        return f"<{name} at {hex(id(self))} ({len(self._commands)} commands)>"

    def __getitem__(self, id: str) -> List[_RegisteredCommand]:
        """Retrieve commands registered under a given ID."""
        return self._commands[id]

    def execute_command(
        self,
        id: str,
        *args: Any,
        execute_asychronously: bool = False,
        **kwargs: Any,
    ) -> Future:
        """Execute a registered command.

        Parameters
        ----------
        id : CommandId
            ID of the command to execute
        execute_asychronously : bool
            Whether to execute the command asynchronously in a thread,
            by default `False`.  Note that *regardless* of this setting,
            the return value will implement the `Future` API (so it's necessary)
            to call `result()` on the returned object.  Eventually, this will
            default to True, but we need to solve `ensure_main_thread` Qt threading
            issues first

        Returns
        -------
        Future: conconrent.futures.Future
            Future object containing the result of the command

        Raises
        ------
        KeyError
            If the command is not registered or has no callbacks.
        """
        if cmds := self[id]:
            # TODO: decide whether we'll ever have more than one command
            # and if so, how to handle it
            cmd = cmds[0].run_injected
        else:
            raise KeyError(
                f'Command "{id}" has no registered callbacks'
            )  # pragma: no cover
        if execute_asychronously:
            with ThreadPoolExecutor() as executor:
                return executor.submit(cmd, *args, **kwargs)
        else:
            future: Future = Future()
            try:
                future.set_result(cmd(*args, **kwargs))
            except Exception as e:
                future.set_exception(e)
            return future

    def __str__(self) -> str:
        lines: list = []
        for id, cmds in self:
            lines.extend(f"{id!r:<32} -> {cmd.title!r}" for cmd in cmds)
        return "\n".join(lines)
